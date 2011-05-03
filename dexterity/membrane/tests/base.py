"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc

from dexterity.membrane.tests.layer import DexterityMembraneLayer

ptc.setupPloneSite(products=['dexterity.membrane'])


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    layer = DexterityMembraneLayer

    def _createType(self, context, portal_type, id):
        """create an object in the proper context
        """
        self.setRoles(('Manager', ))
        ttool = getToolByName(context, 'portal_types')
        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id)
        self.setRoles(())
        obj = getattr(context.aq_inner.aq_explicit, id)
        return obj


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    layer = DexterityMembraneLayer

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
