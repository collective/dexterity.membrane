import unittest

from plone.behavior.interfaces import IBehaviorAssignable
from Products.CMFCore.utils import getToolByName

from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors.metadata import IDublinCore

from dexterity.membrane.membrane_helpers import get_user_id_for_email
from dexterity.membrane.behavior.membraneuser import IMembraneUser
from dexterity.membrane.behavior.membraneuser import IProvidePasswords
from dexterity.membrane.tests.base import TestCase


class TestMember(TestCase):

    def test_create_member(self):
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'jane')
        self.assertEqual(member.portal_type, 'dexterity.membrane.member')

    def test_member_is_membrane_type(self):
        membrane = getToolByName(self.portal, 'membrane_tool')
        self.assertTrue('dexterity.membrane.member' in
                        membrane.listMembraneTypes())
        # Fine, it is a membrane_type, but does it actually work?  We
        # add a member and see if we can find it again using the
        # membrane_tool.

        # Record the current number of members; we do not want this
        # test to fail just because someone adds an extra test member
        # somewhere.
        start_count = len(membrane.unrestrictedSearchResults())
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'jane')
        # Need to reindex the new object manually in the tests (or
        # maybe notify an event).  We would want to just do
        # 'member.reindexObject()' but that is apparently not enough
        # to get it added to the membrane_tool catalog.  Simply adding
        # a member in the live site works though and we do not need to
        # redo the membrane or collective.indexing tests here.
        membrane.reindexObject(member)
        self.assertEqual(len(membrane.unrestrictedSearchResults()),
                         start_count + 1)

    def test_member_properties(self):
        # Some properties from portal_memberdate can be queried from
        # the member content item.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.first_name = 'Joe'
        member.last_name = 'User'
        member.email = 'joe@example.org'
        member.homepage = 'http://example.org/'
        member.bio = u'I am Joe.  I want to set a good example.'
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)
        # Currently the user_id is an intid, so we need to query for
        # that by email/login name:
        user_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertTrue(user_id)
        memship = getToolByName(self.portal, 'portal_membership')
        user = memship.getMemberById(user_id)
        self.failUnless(user)
        self.assertEqual(user.getProperty('fullname'), 'Joe User')
        self.assertEqual(user.getProperty('email'), 'joe@example.org')
        self.assertEqual(user.getProperty('home_page'), 'http://example.org/')
        self.assertEqual(user.getProperty('description'),
                         u'I am Joe.  I want to set a good example.')

    def test_user_name(self):
        # Some upper and lower case issues.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.email = 'JOE@example.org'
        member.password = 'secret'
        member.confirm_password = 'secret'
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)
        # Uppercase:
        user_id = get_user_id_for_email(self.portal, 'JOE@EXAMPLE.ORG')
        self.assertTrue(user_id)
        # Mixed case:
        user_id = get_user_id_for_email(self.portal, 'JOE@example.org')
        self.assertTrue(user_id)
        # Lowercase:
        user_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertTrue(user_id)

        # Real authentication is pickier on the case unfortunately.
        auth = self.portal.acl_users.membrane_users.authenticateCredentials
        credentials = {'login': 'joe@example.org', 'password': 'secret'}
        # First the member needs to be enabled before authentication
        # can succeed.
        self.assertEqual(auth(credentials), None)
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Reviewer'])
        wf_tool.doActionFor(member, 'approve')
        self.setRoles([])
        self.assertEqual(auth(credentials), (user_id, 'joe@example.org'))

        # It would be nice if we could get the next test to pass by
        # setting self.portal.membrane_tool.case_sensitive_auth to
        # False, but this does not work as advertised.
        #credentials = {'login': 'JOE@EXAMPLE.ORG', 'password': 'secret'}
        #self.assertEqual(auth(credentials), (user_id, 'joe@example.org'))

        # Sanity check:
        credentials = {'login': 'otherjoe@example.org', 'password': 'secret'}
        self.assertEqual(auth(credentials), None)

    def test_delete_member(self):
        # Deleting should not leave behind the old brain in the
        # membrane catalog.  Actually, we can just check that an
        # unindexObject works properly.  Note that collective.indexing
        # needs to be available for this, and its monkey patches
        # applied, which should happen automatically on startup.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.email = 'joe@example.org'
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)
        self.assertEqual(len(membrane.unrestrictedSearchResults(
            exact_getUserName='joe@example.org')), 1)
        member.unindexObject()
        self.assertEqual(len(membrane.unrestrictedSearchResults(
            exact_getUserName='joe@example.org')), 0)

    def test_local_roles(self):
        # Members get extra local roles on their own object.
        # Get tools:
        membrane = getToolByName(self.portal, 'membrane_tool')
        memship = getToolByName(self.portal, 'portal_membership')
        # Create joe:
        joe = self._createType(self.portal, 'dexterity.membrane.member', 'joe')
        joe.email = 'joe@example.org'
        membrane.reindexObject(joe)
        joe_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertTrue(joe_id)
        # Create bob:
        bob = self._createType(self.portal, 'dexterity.membrane.member', 'bob')
        bob.email = 'bob@example.org'
        membrane.reindexObject(bob)
        bob_id = get_user_id_for_email(self.portal, 'bob@example.org')
        self.assertTrue(bob_id)
        # Get members:
        joe_member = memship.getMemberById(joe_id)
        self.assertTrue(joe_member)
        bob_member = memship.getMemberById(bob_id)
        self.assertTrue(bob_member)
        # At first, no one gets an extra local role, because the
        # members are not enabled.
        # Test roles of fresh joe:
        self.assertEqual(joe_member.getRolesInContext(self.portal),
                         ['Authenticated'])
        self.assertEqual(joe_member.getRolesInContext(self.portal.bob),
                         ['Authenticated'])
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated'])
        # Test roles of fresh bob:
        self.assertEqual(bob_member.getRolesInContext(self.portal),
                         ['Authenticated'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated'])
        self.assertEqual(bob_member.getRolesInContext(self.portal.joe),
                         ['Authenticated'])
        # We enable/approve both members now.
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Reviewer'])
        wf_tool.doActionFor(joe, 'approve')
        wf_tool.doActionFor(bob, 'approve')
        # Do some reindexing for good measure (alternatively: fire
        # some events).
        #membrane.reindexObject(joe)
        #membrane.reindexObject(bob)
        # Test roles of enabled joe:
        self.assertEqual(joe_member.getRolesInContext(self.portal),
                         ['Authenticated'])
        self.assertEqual(joe_member.getRolesInContext(self.portal.bob),
                         ['Authenticated'])
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated', 'Creator', 'Editor', 'Reader'])
        # Test roles of enabled bob:
        self.assertEqual(bob_member.getRolesInContext(self.portal),
                         ['Authenticated'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated', 'Creator', 'Editor', 'Reader'])
        self.assertEqual(bob_member.getRolesInContext(self.portal.joe),
                         ['Authenticated'])
        # Now disable both members:
        wf_tool.doActionFor(joe, 'disable')
        wf_tool.doActionFor(bob, 'disable')
        # Test the most important roles again:
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated'])

    def test_member_behaviors(self):
        behaviors = [INameFromTitle, IDublinCore, IMembraneUser,
                     IProvidePasswords]
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'les')
        assignable = IBehaviorAssignable(member)
        for b in behaviors:
            self.assertTrue(assignable.supports(b),
                            "member type should support %s behavior" % b)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMember))
    return suite
