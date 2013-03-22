#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent


from dexterity.membrane.interfaces import ICreateMembraneEvent


class CreateMembraneEvent(object):
    interface.implements(ICreateMembraneEvent)
    
    def __init__(self,fullname,password,email,password_ctl):
        """角色,级别,备注"""
        self.fullname = fullname
        self.password = password
        self.email = email
        self.password_ctl = password_ctl