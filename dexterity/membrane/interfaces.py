#-*- coding: UTF-8 -*-
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from dexterity.membrane import  _
# event
class  ICreateMembraneEvent(Interface):
    """新增一个Membrane object"""