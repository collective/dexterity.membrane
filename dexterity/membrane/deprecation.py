# -*- coding: utf-8 -*-
from zope.deprecation import deprecated


def deprecate():
    """provide bbb for deprecations

    note: warnings are not printed unless it is enabled
    """
    from dexterity.membrane import behavior
    from dexterity.membrane.behavior import group
    from dexterity.membrane.behavior import user
    from dexterity.membrane.behavior import password

    behavior.membranegroup = deprecated(
        group,
        'module membranegroup is now named group.'
    )
    behavior.membraneuser = deprecated(
        user,
        'module membraneuser is now named user.'
    )
    behavior.membranepassword = deprecated(
        password,
        'module membranepassword is now named password.'
    )
