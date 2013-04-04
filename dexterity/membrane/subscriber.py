#-*- coding: UTF-8 -*-
import json
from five import grok
from time import strftime, localtime 


from dexterity.membrane.interfaces import ICreateMembraneEvent

from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer

from zope.site.hooks import getSite
from zope.component import getUtility
from plone.uuid.interfaces import IUUID

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import nobody
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()
    def execute_under_special_role(portal, role, function, *args, **kwargs):
        """ Execute code under special role priviledges.
            Example how to call::
            execute_under_special_role(portal, "Manager",
            doSomeNormallyNotAllowedStuff,
            source_folder, target_folder)
            1.13. Security 483
            Plone Developer Manual Documentation, Release
            @param portal: Reference to ISiteRoot object whose access controls we are using
            @param function: Method to be called with special priviledges
            @param role: User role we are using for the security context when calling the priviledged code. For @param args: Passed to the function
            @param kwargs: Passed to the function
            """
        sm = getSecurityManager()
        try:
            try:
                # Clone the current access control user and assign a new role for him/her
                # Note that the username (getId()) is left in exception tracebacks in error_log
                # so it is important thing to store
                tmp_user = UnrestrictedUser(sm.getUser().getId(),
                                            '',
                                            [role],
                                            ''
                                            )
                # Act as user of the portal
                tmp_user = tmp_user.__of__(portal.acl_users)
                newSecurityManager(None, tmp_user)
        # Call the function
                return function(*args, **kwargs)
            except:
# If special exception handlers are needed, run them here
                raise
        finally:
# Restore the old security manager
            setSecurityManager(sm)


@grok.subscribe(ICreateMembraneEvent)
def CreateMembraneEvent(event):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    site = getSite()
    mp = getToolByName(site,'portal_membership')
    members = mp.getMembersFolder()
    if members is None: return      
    catalog = getToolByName(site,'portal_catalog')
    from dexterity.membrane.content.member import IMember     
    try:
        newest = catalog.unrestrictedSearchResults({'object_provides': IMember.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'sort_limit': 1})
        if bool(newest): 
            id = str(int(newest[0].id) + 1)
        else:
            id = str(1000000)              

    except:
            id = str(1000000)  
    item =createContentInContainer(members,"dexterity.membrane.member",checkConstraints=False,id=id)
#    item.id = id    
#    item.id = IUUID(item)
    item.email = event.email
    item.password = event.password
    item.fullname = event.fullname 
    item.password_ctl = event.password_ctl

    membrane = getToolByName(item, 'membrane_tool')      
#    wtool = getToolByName(members, 'portal_workflow')
#    import pdb
#    pdb.set_trace()
#    wtool.doActionFor(item, 'approve')
    membrane.reindexObject(item)
        
