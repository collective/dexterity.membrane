# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IDexterityMembraneSettings(Interface):
    """ Enables through-the-web configuration of some aspects of the
        dexterity.membrane behaviours.
    """

    local_roles = schema.Set(
        title=u'Local Roles',
        description=u'The list of additional local roles members will be '
                    u'granted in the context of their own profile objects',
        value_type=schema.TextLine(),
        required=False,
        missing_value=set([]),
        default=set([]))

    use_email_as_username = schema.Bool(
        title=u'Use email address for username?',
        description=u'If checked, the value in the "email" field will be '
                    u'used as a username/login. If unchecked, your content '
                    u'type must provide a "username" field.',
        required=False)

    use_uuid_as_userid = schema.Bool(
        title=u'Use object UUID for the userid?',
        description=u'If checked, the UUID value for the adapted object '
                    u'will be used for a userid. Otherwise, the username '
                    u'will be used for the userid.',
        required=False)


class DexterityMembraneControlPanelForm(RegistryEditForm):
    schema = IDexterityMembraneSettings


DexterityMembraneControlPanelView = layout.wrap_form(
    DexterityMembraneControlPanelForm,
    ControlPanelFormWrapper
)
