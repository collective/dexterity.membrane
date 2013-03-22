from dexterity.membrane.events import CreateMembraneEvent
from zope import event    
def handle_join_success(self, data):
        # portal should be acquisition wrapped, this is needed for the schema
        # adapter below
#        import pdb
#        pdb.set_trace()
        event.notify(CreateMembraneEvent(data['fullname'],data['password'],data['email'],data['password_ctl']))