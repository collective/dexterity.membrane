# -*- coding: utf-8 -*-
from zope.deprecation import deprecated
import sys


def deprecate():
    """provide bbb for deprecations

    note: warnings are not printed unless it is enabled
    """
    from dexterity.membrane.behavior import password
    from dexterity.membrane.behavior import user
    from dexterity.membrane.behavior import group
    # deprecation
    sys.modules['dexterity.membrane.behavior.membranegroup'] = deprecated(
        group,
        'module membranegroup is now named group.'
    )
    sys.modules['dexterity.membrane.behavior.membraneuser'] = deprecated(
        user,
        'module membraneuser is now named user.'
    )
    sys.modules['dexterity.membrane.behavior.membranepassword'] = deprecated(
        password,
        'module membranepassword is now named password.'
    )
