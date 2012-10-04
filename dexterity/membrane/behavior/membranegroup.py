# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IGroup, IMembraneUserAuth
from five import grok
from zope.interface import Interface


class IMembraneGroup(Interface):
    """Marker interface for Membrane Group"""


class MembraneGroup(object):

    def __init__(self, context):
        self.context = context

    def getGroupId(self):
        return self.context.getId()

    def getGroupName(self):
        return self.context.title

    def getRoles(self):
        return ()

    def getGroupMembers(self):
        mt = getToolByName(self.context, 'membrane_tool')
        usr = mt.unrestrictedSearchResults
        members = {}
        for m in usr(object_implements=IMembraneUserAuth.__identifier__,
                     path='/'.join(self.context.getPhysicalPath())):
            members[m.getUserId] = 1
        return tuple(members.keys())


class MembraneGroupAdapter(grok.Adapter, MembraneGroup):
    grok.context(IMembraneGroup)
    grok.implements(IGroup)
