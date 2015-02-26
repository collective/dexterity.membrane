# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
from dexterity.membrane.deprecation import deprecate

_ = MessageFactory('dexterity.membrane')

# Enable deprecations
deprecate()
