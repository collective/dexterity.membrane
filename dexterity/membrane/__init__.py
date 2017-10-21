# -*- coding: utf-8 -*-
from dexterity.membrane.deprecation import deprecate
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('dexterity.membrane')

# Enable deprecations
deprecate()
