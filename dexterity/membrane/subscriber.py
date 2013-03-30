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

from Products.statusmessages.interfaces import IStatusMessage
from collective.singing import mail

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import nobody
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

#MAIL_NOTIFICATION_TITLE = _(
#    u"mail_notification_title",
#    default=u"'${comment_username}' Back to you to ${thread_title} posts")
#
#MAIL_NOTIFICATION_MESSAGE = _(
#    u"mail_notification_message",
#    default=u"A comment on '${title}' "
#             "has been posted here: ${link}\n\n"
#             "---\n"
#             "${text}\n"
#             "---\n")

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
    membrane.reindexObject(item)
    
#    mail_host = getToolByName(site, 'MailHost')
#    portal_url = getToolByName(site, 'portal_url')
#    portal = portal_url.getPortalObject()
#    sender = portal.getProperty('email_from_address')
#
#    # Check if a sender address is available
#    if not sender:
#        return
#
#
#    # Avoid sending multiple notification emails to the same person
#
#    if not item.email:
#        return 
#
#    
##    sub = obj.Creator()+_(u" Back to you to ")+conversation.title+_(u" posts")
#    sub = safe_unicode(obj.Creator())
#    subject = translate(Message(
#            MAIL_NOTIFICATION_TITLE,
#            mapping={'comment_username':obj.Creator(),
#                    'thread_title':conversation.title}),
#            context=obj.REQUEST)
#    link = portal.absolute_url() + '/login' 
#    message = translate(Message(
#            MAIL_NOTIFICATION_MESSAGE,
#            mapping={'title': safe_unicode(portal.title),
#                     'link': "<a href='"+link+"'>"+link+"</a>",
#                     'text': obj.text.output}),
#            context=obj.REQUEST)
#
#    try:
#
#
#        mail_host.send(mail.create_html_mail(subject,message,'',sender,item.email))
#            
#    except SMTPException:
#        logger.error('SMTP exception while trying to send an ' + 
#                         'email from %s to %s',
#                         sender,
#                         email)
        
