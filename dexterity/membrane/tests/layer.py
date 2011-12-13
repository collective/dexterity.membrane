"""Test layer for dexterity.membrane
"""
from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import installPackage
from Products.PloneTestCase.layer import PloneSite
from Zope2.App import zcml
from Products.Five import fiveconfigure as metaconfigure


class DexterityMembraneLayer(PloneSite):

    @classmethod
    def setUp(cls):
        metaconfigure.debug_mode = True
        import dexterity.membrane
        zcml.load_config('configure.zcml', dexterity.membrane)
        metaconfigure.debug_mode = False
        installPackage('collective.indexing')
        installPackage('dexterity.membrane')

    @classmethod
    def tearDown(cls):
        pass


# When using the defined layer, we need to make sure these Products are
# available:
installProduct('membrane')
