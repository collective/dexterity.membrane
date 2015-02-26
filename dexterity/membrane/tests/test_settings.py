# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.behavior import settings
from dexterity.membrane.testing import DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
import unittest


class TestSettings(unittest.TestCase):

    layer = DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING

    def test_controlpanel_view(self):
        # Test the setting control panel view works
        portal = self.layer['portal']
        view = getMultiAdapter(
            (portal, portal.REQUEST),
            name="dexteritymembrane-settings"
        )
        view = view.__of__(portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        # Test that the setting control panel view can not be
        # accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.layer['portal'].restrictedTraverse,
            '@@dexteritymembrane-settings'
        )

    def test_entry_in_controlpanel(self):
        # Check that there is a dexterity.membrane entry in the control panel
        portal = self.layer['portal']
        controlpanel = getToolByName(portal, "portal_controlpanel")
        actions = [a.getAction(self)['id']
                   for a in controlpanel.listActions()]
        self.assertTrue('DexterityMembraneSettings' in actions)

    def test_registry_defaults(self):
        default_localroles = [u'Creator', u'Editor', u'Reader']
        reg = getUtility(IRegistry)
        config = reg.forInterface(settings.IDexterityMembraneSettings, False)
        self.assertTrue(config)
        self.assertTrue(hasattr(config, 'local_roles'))
        for default in default_localroles:
            self.assertTrue(default in config.local_roles)
        self.assertTrue(hasattr(config, 'use_email_as_username'))
        self.assertTrue(config.use_email_as_username)
        self.assertTrue(hasattr(config, 'use_uuid_as_userid'))
        self.assertTrue(config.use_uuid_as_userid)
