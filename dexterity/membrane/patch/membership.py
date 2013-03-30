from dexterity.membrane.events import CreateMembraneEvent
from Products.statusmessages.interfaces import IStatusMessage
from zope import event
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString, safe_unicode
from Products.CMFPlone import PloneMessageFactory as _

from ZODB.POSException import ConflictError
from zExceptions import Forbidden
    
def handle_join_success(self, data):
        # portal should be acquisition wrapped, this is needed for the schema
        # adapter below
#        import pdb
#        pdb.set_trace()


        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        registration = getToolByName(self.context, 'portal_registration')
        portal_props = getToolByName(self.context, 'portal_properties')
        mt = getToolByName(self.context, 'portal_membership')
        props = portal_props.site_properties
        use_email_as_login = props.getProperty('use_email_as_login')        

        if use_email_as_login:
            # The username field is not shown as the email is going to
            # be the username, but the field *is* needed further down
            # the line.
            data['username'] = data['email']
            # Set username in the form; at least needed for logging in
            # immediately when password reset is bypassed.
            self.request.form['form.username'] = data['email']

        user_id = data['username']
        password = data.get('password') or registration.generatePassword()
        if isinstance(password, unicode):
            password = password.encode('utf8')

        try:
            event.notify(CreateMembraneEvent(data['fullname'],password,data['email'],password))
#            event.notify(CreateMembraneEvent(data['fullname'],data['password'],data['email'],data['password_ctl']))            
        except (AttributeError, ValueError), err:
            logging.exception(err)
            IStatusMessage(self.request).addStatusMessage(err, type="error")
            return

        # set additional properties using the user schema adapter
#        schema = getUtility(IUserDataSchemaProvider).getSchema()
#
#        adapter = getAdapter(portal, schema)
#        adapter.context = mt.getMemberById(user_id)
#
#        for name in getFieldNamesInOrder(schema):
#            if name in data:
#                setattr(adapter, name, data[name])

        if data.get('mail_me') or (portal.validate_email and
                                   not data.get('password')):
            # We want to validate the email address (users cannot
            # select their own passwords on the register form) or the
            # admin has explicitly requested to send an email on the
            # 'add new user' form.
            try:
                # When all goes well, this call actually returns the
                # rendered mail_password_response template.  As a side
                # effect, this removes any status messages added to
                # the request so far, as they are already shown in
                # this template.
                response = registration.registeredNotify(user_id)
                IStatusMessage(self.request).addStatusMessage(
                        _(u'create_membrane_account_succesful',
                          default=u"Your account has been created,we "
                          "have sent instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': data.get('email', '')}),
                        type='info')
                return response
            except ConflictError:
                # Let Zope handle this exception.
                raise
            except Exception:
                ctrlOverview = getMultiAdapter((portal, self.request),
                                               name='overview-controlpanel')
                mail_settings_correct = not ctrlOverview.mailhost_warning()
                if mail_settings_correct:
                    # The email settings are correct, so the most
                    # likely cause of an error is a wrong email
                    # address.  We remove the account:
                    # Remove the account:
                    self.context.acl_users.userFolderDelUsers(
                        [user_id], REQUEST=self.request)
                    IStatusMessage(self.request).addStatusMessage(
                        _(u'status_fatal_password_mail',
                          default=u"Failed to create your account: we were "
                          "unable to send instructions for setting a password "
                          "to your email address: ${address}",
                          mapping={u'address': data.get('email', '')}),
                        type='error')
                    return
                else:
                    # This should only happen when an admin registers
                    # a user.  The admin should have seen a warning
                    # already, but we warn again for clarity.
                    IStatusMessage(self.request).addStatusMessage(
                        _(u'status_nonfatal_password_mail',
                          default=u"This account has been created, but we "
                          "were unable to send instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': data.get('email', '')}),
                        type='warning')
                    return

        return        