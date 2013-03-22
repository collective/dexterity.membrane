from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.member import IMember 

from dexterity.membrane.behavior.membraneuser import IProvidePasswords 
from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity

grok.templatedir('templates')

class MemberView(grok.View):
    grok.context(IMember)     
    grok.template('member_view')
    grok.name('view')
    grok.require('zope2.View')


    def language(self):        
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        current_language = portal_state.language()
        return current_language
    
    def fullname(self):
        context = self.context
#        import pdb
#        pdb.set_trace()
        if self.language() == 'en':            
                names = [
                         context.first_name,
                         context.last_name,
                         ]
                return u' '.join([name for name in names if name])
        else:
                names = [
                         context.last_name,                         
                         context.first_name,
                         ]            
                return u''.join([name for name in names if name])            
    
class EditProfile(dexterity.EditForm):
    grok.name('edit-baseinfo')
    grok.context(IMember)    
    label = _(u'Base information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('last_name','first_name','email','bio','photo')

class EditProfilePassword(dexterity.EditForm):
    grok.name('edit-password')
    grok.context(IMember)    
    label = _(u'Update password')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IProvidePasswords).select('password','confirm_password')

class EditProfileNetworking(dexterity.EditForm):
    grok.name('edit-networking')
    grok.context(IMember)    
    label = _(u'Network information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('homepage', 'phone','qq_number')
        
class EditProfileWork(dexterity.EditForm):
    grok.name('edit-work')
    grok.context(IMember)    
    label = _(u'Work information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('organization','sector','position','research_domain')

class EditProfileGeography(dexterity.EditForm):
    grok.name('edit-geography')
    grok.context(IMember)    
    label = _(u'Geography information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('country', 'province','address')