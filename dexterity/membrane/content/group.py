# -*- coding: utf-8 -*-
from dexterity.membrane import _
from dexterity.membrane.membrane_helpers import validate_unique_email
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import Invalid, invariant
import re


class IGroup(model.Schema):
    """Group"""

