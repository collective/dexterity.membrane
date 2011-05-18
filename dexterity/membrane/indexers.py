from plone.indexer.decorator import indexer

from dexterity.membrane.content.member import IMember
from dexterity.membrane.behavior.membraneuser import INameFromFullName


@indexer(IMember)
def Title(object, **kw):
    name = INameFromFullName(object, None)
    if name is not None:
        return name.title
    return object.Title()
