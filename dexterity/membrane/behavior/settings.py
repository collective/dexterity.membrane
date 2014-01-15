from zope.interface import Interface
from zope import schema

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout

from dexterity.membrane import _

local_roles_desc = u"""
The list of additional local roles members will be granted in the context
of their own profile objects
"""
use_email_as_username_desc = u"""
If checked, the value in the "email" field will be used as a username/login.
If unchecked, your content type must provide a "username" field.
"""
use_uuid_as_userid_desc = u"""
If checked, the UUID value for the adapted object will be used for a userid.
Otherwise, the username will be used for the userid.
"""


class IDexterityMembraneSettings(Interface):
    """ Enables through-the-web configuration of some aspects of the
        dexterity.membrane behaviours.
    """

    properties_whitelist = schema.Set(
        title=_(u'Properties whitelist'),
        description=_(u'The list of properties to fetch in the user object.'),
        value_type=schema.ASCIILine(title=_(u'Property')),
        required=False,
        missing_value=set([]),
        default=set([]),
    )

    local_roles = schema.Set(
        title=_(u'Local Roles'),
        description=_(u'local_roles',
                      default=local_roles_desc),
        value_type=schema.TextLine(),
        required=False,
        missing_value=set([]),
        default=set([])
    )

    use_email_as_username = schema.Bool(
        title=_(u'Use email address for username?'),
        description=_(u'use_email_address_for_username',
                      default=use_email_as_username_desc),
        required=False
    )

    use_uuid_as_userid = schema.Bool(
        title=_(u'Use object UUID for the userid?'),
        description=_(u'use_uuid_as_userid_desc',
                      default=use_uuid_as_userid_desc),
        required=False
    )


class DexterityMembraneControlPanelForm(RegistryEditForm):
    schema = IDexterityMembraneSettings


DexterityMembraneControlPanelView = layout.wrap_form(
    DexterityMembraneControlPanelForm, ControlPanelFormWrapper)
