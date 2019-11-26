# coding=utf-8
from logging import getLogger
from plone import api
from plone.dexterity.interfaces import IDexterityFTI


logger = getLogger(__name__)


def move_dotted_to_named_behaviors(context):
    """ https://github.com/plone/plone.app.upgrade/blob/master/plone/app/upgrade/v52/alphas.py#L58  # noqa: E501
    """
    mapping = {
        "dexterity.membrane.behavior.group.IMembraneGroup": "dexterity.membrane.group",
        "dexterity.membrane.behavior.password.IProvidePasswords": "dexterity.membrane.provide_password",  # noqa: E501
        "dexterity.membrane.behavior.user.IMembraneUser": "dexterity.membrane.user",
        "dexterity.membrane.behavior.user.INameFromFullName": "dexterity.membrane.name_from_fullname",  # noqa: E501
    }

    ptt = api.portal.get_tool("portal_types")
    ftis = (fti for fti in ptt.objectValues() if IDexterityFTI.providedBy(fti))
    for fti in ftis:
        behaviors = []
        change_needed = False
        for behavior in fti.behaviors:
            if behavior in mapping:
                behavior = mapping[behavior]
                change_needed = True
            behaviors.append(behavior)
        if change_needed:
            fti.behaviors = tuple(behaviors)

    logger.info("Done moving dotted to named behaviors.")
