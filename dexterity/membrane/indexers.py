# -*- coding: utf-8 -*-
from dexterity.membrane.behavior.user import INameFromFullName
from dexterity.membrane.content.member import IMember
from plone.indexer.decorator import indexer


@indexer(IMember)
def Title(object, **kw):
    name = INameFromFullName(object, None)
    if name is not None:
        return name.title
    return object.Title()
