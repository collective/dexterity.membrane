# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME
from dexterity.membrane import _
from zope.component.hooks import getSite
import logging


logger = logging.getLogger(__name__)


def get_brains_for_email(context, email, request=None):
    """Anonymous users should be able to look for email addresses.
    Otherwise they cannot log in.

    This searches in the membrane_tool and returns brains with this
    email address.  Hopefully the result is one or zero matches.

    Note that we search for exact_getUserName as the email address is
    supposed to be used a login name (user name).  TODO: We may want
    to change the name of this function to reflect this.
    """
    try:
        email = email.strip()
    except (ValueError, AttributeError):
        return []
    if email == '' or '@' not in email:
        return []

    user_catalog = getToolByName(context, TOOLNAME, None)
    if user_catalog is None:
        logger.warn("membrane_tool not found.")
        return []

    # if request is None:
    #     try:
    #         request = context.REQUEST
    #     except:
    #         # Happens e.g. when submitting a change in the
    #         # prefs_user_overview.  Just use None.
    #         pass
    kw = dict(exact_getUserName=email)
    # args = CatalogSearchArgumentsMap(request, kw)
    # users = user_catalog.search(args)
    users = user_catalog.unrestrictedSearchResults(**kw)
    return users


def get_user_id_for_email(context, email):
    brains = get_brains_for_email(context, email)
    if len(brains) == 1:
        return brains[0].getUserId
    return ''


def validate_unique_email(email, context=None):
    """Validate this email as unique in the site.
    """
    if context is None:
        context = getSite()
    matches = get_brains_for_email(context, email)
    if not matches:
        # This email is not used yet.  Fine.
        return
    if len(matches) > 1:
        msg = "Multiple matches on email %s" % email
        logger.warn(msg)
        return msg
    # Might be this member, being edited.  That should have been
    # caught by our new invariant though, at least when changing the
    # email address through the edit interface instead of a
    # personalize_form.
    match = matches[0]
    try:
        found = match.getObject()
    except (AttributeError, KeyError, Unauthorized):
        # This is suspicious.  Best not to use this one.
        pass
    else:
        if found == context:
            # We are the only match.  Good.
            logger.debug("Only this object itself has email %s", email)
            return

    # There is a match but it is not this member or we cannot get
    # the object.
    msg = _("Email ${email} is already in use.", mapping={'email': email})
    logger.debug(msg)
    return msg


def get_membrane_user(context, principal_id, member_type='nd.content.member',
                      get_object=False):
    catalog = getToolByName(context, TOOLNAME, None)
    if catalog is None:
        logger.debug("membrane_tool not found.")
        # Probably just the admin user, in which case we can just
        # return nothing.
        return None

    res = catalog(exact_getUserId=principal_id, portal_type=member_type)
    if len(res) != 1:
        return None
    brain = res[0]
    if get_object:
        return brain.getObject()
    return brain


def safe_encode(string):
    """Safely unicode objects to UTF-8. If it's a binary string, just return
    it.
    """
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    return string
