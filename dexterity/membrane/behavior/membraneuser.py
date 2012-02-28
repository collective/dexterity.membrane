import logging

from AccessControl.AuthEncoding import pw_encrypt
from AccessControl.AuthEncoding import pw_validate
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserChanger
from Products.membrane.interfaces import IMembraneUserObject
from Products.membrane.interfaces import IMembraneUserProperties
from five import grok
from plone.app.content.interfaces import INameFromTitle
from plone.directives import form
from plone.uuid.interfaces import IUUID
from z3c.form.interfaces import IAddForm
from zope import schema
from zope.component import adapts
from zope.component import getUtility
from zope.interface import alsoProvides, implements
from zope.interface import Interface, invariant, Invalid

from dexterity.membrane import _

logger = logging.getLogger(__name__)


class IMembraneUser(Interface):
    """Marker/Form interface for Membrane User

    The main content schema of the membrane user must contain fields named
    'first_name', 'last_name', and 'email'.

    The content item must also be adaptable to IProvidePasswords.
    """


def get_full_name(context):
    names = [
        context.first_name,
        context.last_name,
        ]
    return u' '.join([name for name in names if name])


class INameFromFullName(INameFromTitle):
    """Get the name from the full name.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class NameFromFullName(object):
    implements(INameFromFullName)
    adapts(IMembraneUser)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return get_full_name(self.context)


class IMembraneUserWorkflow(Interface):
    """Adapts a membrane user to provide workflow-related info."""

    def is_right_state(self):
        """Returns true if the user is in a state considered active."""


class MembraneUser(object):
    """Methods for Membrane User
    """

    allowed_states = ('enabled',)
    _default = {'use_email_as_username': True,
                'use_uuid_as_userid': True}

    def __init__(self, context):
        self.context = context

    def in_right_state(self):
        workflow = getToolByName(self.context, 'portal_workflow')
        state = workflow.getInfoFor(self.context, 'review_state')
        return state in self.allowed_states

    def getUserId(self):
        if self._use_uuid_as_userid():
            return IUUID(self.context)
        return self.getUserName()

    def getUserName(self):
        if self._use_email_as_username():
            return self.context.email.lower()
        return self.context.username

    def _use_email_as_username(self):
        return self._reg_setting('use_email_as_username')

    def _use_uuid_as_userid(self):
        return self._reg_setting('use_uuid_as_userid')

    def _reg_setting(self, setting):
        reg = getUtility(IRegistry)
        config = reg.forInterface(settings.IDexterityMembraneSettings, False)
        if config and hasattr(config, setting):
            return getattr(config, setting)
        return self._default(setting)


class MembraneUserAdapter(grok.Adapter, MembraneUser):
    grok.context(IMembraneUser)
    grok.implements(IMembraneUserObject)


class MembraneUserWorkflow(grok.Adapter, MembraneUser):
    grok.context(IMembraneUser)
    grok.implements(IMembraneUserWorkflow)


class MyUserAuthentication(grok.Adapter):
    grok.context(IMembraneUser)
    grok.implements(IMembraneUserAuth)

    def verifyCredentials(self, credentials):
        """Returns True is password is authenticated, False if not.
        """
        user = IMembraneUserObject(self.context)
        if credentials.get('login').lower() != user.getUserName().lower():
            # Should never happen, as the code should then never end
            # up here, but better safe than sorry.
            return False
        password_provider = IProvidePasswords(self.context)
        if not password_provider:
            return False
        return pw_validate(password_provider.password,
                           credentials.get('password', ''))

    def authenticateCredentials(self, credentials):
        # Should not authenticate when the user is not enabled.
        workflow_info = IMembraneUserWorkflow(self.context)
        if not workflow_info.in_right_state():
            return
        if self.verifyCredentials(credentials):
            # return (self.getUserId(), self.getUserName())
            user = IMembraneUserObject(self.context)
            return (user.getUserId(), user.getUserName())


class IProvidePasswords(form.Schema):
    """Add password fields"""

    # Putting this in a separate fieldset for the moment:
    form.fieldset('membership', label=_(u"Membership"),
                  fields=['password', 'confirm_password'])

    # Note that the passwords fields are not required; this means we
    # can add members without having to add passwords at that time.
    # The password reset tool should hopefully be able to deal with
    # that.
    password = schema.Password(
        title=_(u"Password"),
        required=False,
    )

    confirm_password = schema.Password(
        title=_(u"Confirm Password"),
        required=False,
    )

    @invariant
    def password_matches_confirmation(data):
        """password field must match confirm_password field.
        """
        password = getattr(data, 'password', None)
        confirm_password = getattr(data, 'confirm_password', None)
        if (password or confirm_password) and (password != confirm_password):
            raise Invalid(_(u"The password and confirmation do not match."))

    form.omitted('password', 'confirm_password')
    form.no_omit(IAddForm, 'password', 'confirm_password')


alsoProvides(IProvidePasswords, form.IFormFieldProvider)


class PasswordProvider(object):

    def __init__(self, context):
        self.context = context

    def _get_password(self):
        return getattr(self.context, 'password', None)

    def _set_password(self, password):
        # When editing, the password field is empty in the browser; do
        # not do anything then.
        if password is not None:
            self.context.password = pw_encrypt(password)

    def _get_confirm_password(self):
        # Just return the original password.
        return self._get_password()

    def _set_confirm_password(self, confirm_password):
        # No need to store this.
        return

    password = property(_get_password, _set_password)
    confirm_password = property(_get_confirm_password, _set_confirm_password)


class PasswordProviderAdapter(grok.Adapter, PasswordProvider):
    grok.context(IMembraneUser)
    grok.implements(IProvidePasswords)


class MyUserPasswordChanger(grok.Adapter, MembraneUser):
    """Supports resetting a member's password via the password reset form."""
    grok.context(IMembraneUser)
    grok.implements(IMembraneUserChanger)

    def doChangeUser(self, user_id, password, **kwargs):
        password_provider = IProvidePasswords(self.context)
        password_provider.password = password


class MyUserProperties(grok.Adapter, MembraneUser):
    """User properties for this membrane context.

    Adapted from Products/membrane/at/properties.py
    """

    grok.context(IMembraneUser)
    grok.implements(IMembraneUserProperties)

    # Map from memberdata property to member field:
    property_map = dict(
        email='email',
        home_page='homepage',
        description='bio',
        )

    @property
    def fullname(self):
        # Note: we only define a getter; a setter would be too tricky
        # due to the multiple fields that are behind this one
        # property.
        return get_full_name(self.context)

    def getPropertiesForUser(self, user, request=None):
        """Get properties for this user.

        Find the fields of the user schema that make sense as a user
        property in @@personal-information.

        Note: this method gets called a crazy amount of times...

        Also, it looks like we can ignore the user argument and just
        check self.context.
        """
        properties = dict(
            fullname=self.fullname,
            )
        for prop_name, field_name in self.property_map.items():
            value = getattr(self.context, field_name)
            if value is None:
                # Would give an error like this:
                # ValueError: Property home_page: unknown type
                value = u''
            properties[prop_name] = value
        return MutablePropertySheet(self.context.getId(),
                                    **properties)

    def setPropertiesForUser(self, user, propertysheet):
        """
        Set modified properties on the user persistently.

        Should raise a ValueError if the property or property value is
        invalid.  We choose to ignore it and just handpick the ones we
        like.

        For example, fullname cannot be handled as we don't know how
        to split that into first, middle and last name.
        """
        properties = dict(propertysheet.propertyItems())
        for prop_name, field_name in self.property_map.items():
            value = properties.get(prop_name, '').strip()
            logger.debug("Setting field %s: %r", field_name, value)
            setattr(self.context, field_name, value)

    def deleteUser(self, user_id):
        """
        Remove properties stored for a user

        Note that membrane itself does not do anything here.  This
        indeed seems unneeded, as the properties are stored on the
        content item, so they get removed anyway without needing
        special handling.
        """
        pass


from borg.localrole.interfaces import ILocalRoleProvider
from plone.registry.interfaces import IRegistry
from dexterity.membrane.behavior import settings


class MembraneRoleProvider(object):
    # Give a membrane user some extra local roles in his/her own member
    # object.
    implements(ILocalRoleProvider)
    adapts(IMembraneUser)

    _default_roles = ('Reader', 'Editor', 'Creator')

    def __init__(self, context):
        self.context = context
        self.roles = self._roles()

    def _roles(self):
        reg = getUtility(IRegistry)
        config = reg.forInterface(settings.IDexterityMembraneSettings, False)
        if config and config.local_roles is not None:
            return tuple(config.local_roles)
        return self._default_roles

    def _in_right_state(self):
        workflow_info = IMembraneUserWorkflow(self.context)
        return workflow_info.in_right_state()

    def getRoles(self, user_id):
        membrane = IMembraneUserObject(self.context)
        if membrane.getUserId() != user_id:
            return ()
        if not self._in_right_state():
            return ()
        return self.roles

    def getAllRoles(self):
        """Here we should apparently enumerate all users who should
        get an extra role.
        """
        if not self._in_right_state():
            return
        membrane = IMembraneUserObject(self.context)
        yield membrane.getUserId(), self.roles
