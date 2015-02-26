# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.membrane.interfaces import IMembraneUserObject
from Products.membrane.interfaces import IMembraneUserProperties
from borg.localrole.interfaces import ILocalRoleProvider
from dexterity.membrane.behavior import settings
from plone.app.content.interfaces import INameFromTitle
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implementer
import logging

logger = logging.getLogger(__name__)


class IMembraneUser(Interface):
    """Marker/Form interface for Membrane User

    XXX: Bad Name, since its used for something different in Products.Membrane

    The main content schema of the membrane user must contain fields named
    'first_name', 'last_name', and 'email'.

    The content item must also be adaptable to IProvidePasswords.
    """


class INameFromFullName(INameFromTitle):
    """Get the name from the full name.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class IMembraneUserWorkflow(Interface):
    """Adapts a membrane user to provide workflow-related info."""

    def in_right_state(self):
        """Returns true if the user is in a state considered active."""


@implementer(INameFromFullName)
@adapter(IMembraneUser)
class NameFromFullName(object):

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return IMembraneUserObject(self.context).get_full_name()


class DxUserObject(object):
    """Base Behavioral Methods for Membrane User
    """

    _default = {'use_email_as_username': True,
                'use_uuid_as_userid': True}

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        if self._use_uuid_as_userid():
            return IUUID(self.context)
        return self.getUserName()

    def getUserName(self):
        if self._use_email_as_username():
            return self.context.email
        return self.context.username

    def get_full_name(self):
        names = [
            self.context.first_name,
            self.context.last_name,
            ]
        return u' '.join([name for name in names if name])

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


@implementer(IMembraneUserObject)
@adapter(IMembraneUser)
class MembraneUserObject(DxUserObject):
    pass


@implementer(IMembraneUserWorkflow)
@adapter(IMembraneUser)
class MembraneUserWorkflow(DxUserObject):

    allowed_states = ('enabled',)

    def in_right_state(self):
        workflow = getToolByName(self.context, 'portal_workflow')
        state = workflow.getInfoFor(self.context, 'review_state')
        return state in self.allowed_states


@implementer(IMembraneUserProperties)
@adapter(IMembraneUser)
class MembraneUserProperties(DxUserObject):
    """User properties for this membrane context.

    Adapted from Products/membrane/at/properties.py
    """

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
        return IMembraneUserObject(self.context).get_full_name()

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
            value = getattr(self.context, field_name, None)
            if value is None:
                # Would give an error like this:
                # ValueError: Property home_page: unknown type
                value = u''
            properties[prop_name] = value
        return MutablePropertySheet(self.context.getId(), **properties)

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


@implementer(ILocalRoleProvider)
@adapter(IMembraneUser)
class MembraneRoleProvider(object):
    # Give a membrane user some extra local roles in his/her own member
    # object.

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
