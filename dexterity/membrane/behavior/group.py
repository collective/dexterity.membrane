# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IGroup
from Products.membrane.interfaces import IMembraneUserAuth
from zope.interface import Interface
from zope.component import adapter
from zope.interface import implementer


class IMembraneGroup(Interface):
    """Marker interface for Membrane Group"""


@implementer(IGroup)
@adapter(IMembraneGroup)
class MembraneGroup(object):

    def __init__(self, context):
        self.context = context

    def getGroupId(self):
        return self.context.getId()

    def getGroupName(self):
        return self.context.title

    # A group might accidentally show up as a user.
    # portal_membership.listMembers then says:
    # AttributeError: 'NoneType' object has no attribute '__of__'
    # We prevent this by implementing getUserId and getUserName.
    getUserId = getGroupId
    getUserName = getGroupName

    def getRoles(self):
        return ()

    def getGroupMembers(self):
        mt = getToolByName(self.context, 'membrane_tool')
        brains = mt.unrestrictedSearchResults(
            object_implements=IMembraneUserAuth.__identifier__,
            path='/'.join(self.context.getPhysicalPath())
        )
        return tuple(set([_.m.getUserId for _ in brains]))
