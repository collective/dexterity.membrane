from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from dexterity.membrane.behavior import settings
from dexterity.membrane.tests.base import TestCase


class TestSettings(TestCase):

    def test_controlpanel_view(self):
        # Test the membership setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="dexteritymembrane-settings")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        # Test that the membership setting control panel view can not be
        # accessed by anonymous users
        from AccessControl import Unauthorized
        self.logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                                    '@@dexteritymembrane-settings')

    def test_roles_in_controlpanel(self):
        # Check that there is an membership entry in the control panel
        controlpanel = getToolByName(self.portal, "portal_controlpanel")
        actions = [a.getAction(self)['id']
                            for a in controlpanel.listActions()]
        self.assertTrue('DexterityMembraneSettings' in actions)

    def test_registry_defaults(self):
        defaults = [u'Creator', u'Editor', u'Reader']
        reg = getUtility(IRegistry)
        config = reg.forInterface(settings.IDexterityMembraneSettings, False)
        self.assertTrue(config)
        self.assertTrue(hasattr(config, 'local_roles'))
        for default in defaults:
            self.assertTrue(default in config.local_roles)
