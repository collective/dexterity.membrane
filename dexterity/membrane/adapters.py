from five import grok
from Products.membrane.interfaces import IMembraneUserRoles
from dexterity.membrane.behavior.membraneuser import MembraneUser

class MemberRoleProvider(grok.Adapter, MembraneUser):
    from dexterity.membrane.content.member import IMember
    grok.context(IMember)
    grok.implements(IMembraneUserRoles)
    def __init__(self, context):
        self.context = context
    def getRolesForPrincipal(self, principal, request=None):
            roles = []
            bonus = self.context.bonus
            if bonus > 1000:
                roles.append('Site Administrator')

            if bonus > 100:
                roles.append('Paid Member')
            else:
                roles.append('Member')                
            return roles