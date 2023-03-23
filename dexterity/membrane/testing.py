# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig

try:
    from plone.testing import zope as zope_testing
except ImportError:
    # Plone 5.1 compatibility
    from plone.testing import z2 as zope_testing


CONTENT_PROFILE = 'dexterity.membrane.content:content'

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
        # plone.app.referenceablebehavior can be added with the extra [archetypes]
        try:
            import plone.app.referenceablebehavior
            xmlconfig.file(
                'configure.zcml',
                plone.app.referenceablebehavior,
                context=configurationContext
            )
        except ImportError:
            pass
        zope_testing.installProduct(app, 'Products.membrane')

    def setUpPloneSite(self, portal):
        applyProfile(portal, CONTENT_PROFILE)
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
