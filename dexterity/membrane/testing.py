# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope as zope_testing
from zope.configuration import xmlconfig


EXAMPLE_PROFILE = 'dexterity.membrane.content:example'

CONTRIBUTOR_NAME = 'contributor'
REVIEWER_NAME = 'reviewer'


class DexterityMembrane(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import dexterity.membrane
        xmlconfig.file(
            'configure.zcml',
            dexterity.membrane,
            context=configurationContext
        )
        import plone.app.referenceablebehavior
        xmlconfig.file(
            'configure.zcml',
            plone.app.referenceablebehavior,
            context=configurationContext
        )
        zope_testing.installProduct(app, 'Products.membrane')

    def setUpPloneSite(self, portal):
        applyProfile(portal, EXAMPLE_PROFILE)
        portal.portal_workflow.setDefaultChain('one_state_workflow')

    def tearDownZope(self, app):
        zope_testing.uninstallProduct(app, 'Products.membrane')


DEXTERITY_MEMBRANE_FIXTURE = DexterityMembrane()
DEXTERITY_MEMBRANE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DEXTERITY_MEMBRANE_FIXTURE,),
    name="DexterityMembrane:Integration"
)
DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DEXTERITY_MEMBRANE_FIXTURE,),
    name="DexterityMembrane:Functional"
)
