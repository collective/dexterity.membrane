"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

from dexterity.membrane.tests.layer import DexterityMembraneLayer


CONTENT_PROFILE = 'dexterity.membrane.content:content'
BEHAVIOR_PROFILE = 'dexterity.membrane:behavior'


# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    """
    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.
    fiveconfigure.debug_mode = True
    import dexterity.membrane
    zcml.load_config('configure.zcml', dexterity.membrane)
    fiveconfigure.debug_mode = False
    ztc.installPackage('dexterity.membrane')

setup_product()
ptc.setupPloneSite(extension_profiles=[CONTENT_PROFILE, BEHAVIOR_PROFILE])


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
