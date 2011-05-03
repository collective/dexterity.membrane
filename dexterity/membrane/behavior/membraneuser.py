import logging
from AccessControl.AuthEncoding import pw_encrypt
from AccessControl.AuthEncoding import pw_validate
from five import grok
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import invariant, Invalid
from zope.interface import implements
from zope import schema
from plone.directives import form
#from plone.dexterity.interfaces import IDexterityContent
#from plone.autoform.interfaces import IFormFieldProvider

from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserObject
from Products.membrane.interfaces import IMembraneUserProperties
from Products.PlonePAS.sheet import MutablePropertySheet
from plone.uuid.interfaces import IUUID

from dexterity.membrane import _
from dexterity.membrane.content.member import IEmail
from dexterity.membrane.content.member import IMember

logger = logging.getLogger(__name__)


class IMembraneUser(form.Schema):
    """
       Marker/Form interface for Membrane User
    """


#alsoProvides(IMembraneUser, IFormFieldProvider)


class MembraneUser(object):
    """Methods for Membrane User
    """

    allowed_states = ('enabled', )

    def __init__(self, context):
        self.context = context

    def in_right_state(self):
        """Is the context in an allowed review state?
        """
        workflow = getToolByName(self.context, 'portal_workflow')
        state = workflow.getInfoFor(self.context, 'review_state')
        return state in self.allowed_states

    def getUserId(self):
        return IUUID(self.context)

    def getUserName(self):
        # The email address is the login name.  We force lower case.
        return self.context.email.lower()


class MembraneUserAdapter(grok.Adapter, MembraneUser):
    grok.context(IEmail)
    grok.implements(IMembraneUserObject)


class MyUserAuthentication(grok.Adapter, MembraneUser):
    grok.context(IEmail)  # Needs IProvidePasswords too, really.
    grok.implements(IMembraneUserAuth)

    def verifyCredentials(self, credentials):
        """Returns True is password is authenticated, False if not.
        """
        if credentials.get('login') != self.getUserName():
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
        if not self.in_right_state():
            return
        if self.verifyCredentials(credentials):
            return (self.getUserId(), self.getUserName())


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
        # TODO: store hashed
    )

    confirm_password = schema.Password(
        title=_(u"Confirm Password"),
        required=False,
    )

    @invariant
    def password_matches_confirmation(data):
        """password field must match confirm_password field.
        """
        if data.password != data.confirm_password:
            raise Invalid(_(u"The password and confirmation do not match."))

    # TODO: Hide the password fields when viewing.


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
    grok.context(IEmail)
    grok.implements(IProvidePasswords)


class MyUserProperties(grok.Adapter, MembraneUser):
    """User properties for this membrane context.

    Adapted from Products/membrane/at/properties.py
    """

    grok.context(IMember)
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
        # property.  Possibly add middle_name and maybe suffix, but we
        # don't do that in the Lilly project either.
        names = [
            self.context.first_name,
            self.context.last_name,
            ]
        return u' '.join([name for name in names if name])

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


class MembraneRoleProvider(object):
    # Give a membrane user some extra local roles in his own member
    # object.
    implements(ILocalRoleProvider)
    adapts(IEmail)
    roles = ('Reader', 'Editor', 'Creator')

    def __init__(self, context):
        self.context = context

    def getRoles(self, user_id):
        membrane = IMembraneUserObject(self.context)
        if membrane.getUserId() != user_id:
            return ()
        if not membrane.in_right_state():
            return ()
        return self.roles

    def getAllRoles(self):
        """Here we should apparently enumerate all users who should
        get an extra role.
        """
        membrane = IMembraneUserObject(self.context)
        if not membrane.in_right_state():
            return
        yield membrane.getUserId(), self.roles
