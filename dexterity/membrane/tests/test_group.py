# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserObject
from dexterity.membrane.behavior.user import IMembraneUser
from dexterity.membrane.behavior.password import IProvidePasswords
from dexterity.membrane.testing import DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING
from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors import metadata
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.behavior.interfaces import IBehaviorAssignable
from plone import api
import unittest


class TestGroup(unittest.TestCase):

    layer = DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING

    def _createType(self, context, portal_type, id):
        """create an object in the proper context
        """
        login(self.layer['portal'], TEST_USER_NAME)
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])
        ttool = getToolByName(context, 'portal_types')
        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id)
        obj = getattr(context.aq_inner.aq_explicit, id)
        return obj

    def test_create_group(self):
        group = self._createType(
            self.layer['portal'], 'dexterity.membrane.group', 'staff')
        self.assertEqual(group.portal_type, 'dexterity.membrane.group')

    def test_group_is_membrane_type(self):
        membrane = getToolByName(self.layer['portal'], 'membrane_tool')
        self.assertTrue(
            'dexterity.membrane.group' in membrane.listMembraneTypes()
        )
        # Fine, it is a membrane_type, but does it actually work?  We
        # add a group and see if we can find it again using the
        # membrane_tool.

        # Record the current # of dexterity.membrane content; we do not
        # want this test to fail just because someone adds more somewhere.
        start_count = len(membrane.unrestrictedSearchResults())
        group = self._createType(
            self.layer['portal'],
            'dexterity.membrane.group',
            'staff'
        )
        # Need to reindex the new object manually in the tests (or
        # maybe notify an event).  We would want to just do
        # 'group.reindexObject()' but that is apparently not enough
        # to get it added to the membrane_tool catalog.  Simply adding
        # a group in the live site works though and we do not need to
        # redo the membrane or collective.indexing tests here.
        membrane.reindexObject(group)
        self.assertEqual(
            len(membrane.unrestrictedSearchResults()),
            start_count + 1
        )

    def test_member_of_group(self):

        membrane = api.portal.get_tool("membrane_tool")
        membership = api.portal.get_tool("portal_membership")
        groups = api.portal.get_tool("portal_groups")

        # Add a group and a member inside it.

        staff = self._createType(
            self.layer["portal"],
            "dexterity.membrane.group",
            "staff"
        )
        membrane.reindexObject(staff)
        group = groups.getGroupById("staff")
        self.failUnless(group)

        joedoe = self._createType(
            staff,
            "dexterity.membrane.member",
            "joedoe"
        )
        membrane.reindexObject(joedoe)
        user = membership.getMemberById(joedoe.UID())
        self.failUnless(user)

        # Added user should be listed in group's users and inherit the Manager
        # role assigned to the group.
        members = api.user.get_users(groupname='staff')
        # user != members[0], need to go deeper..
        self.assertTrue(user.aq_base.id == members[0].aq_base.id)
        self.assertTrue("Manager" not in api.group.get_roles(group=group))
        api.group.grant_roles(group=group, roles=["Manager"])
        user_roles = api.user.get_roles(user=user)
        self.assertTrue("Manager" in user_roles)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGroup))
    return suite
