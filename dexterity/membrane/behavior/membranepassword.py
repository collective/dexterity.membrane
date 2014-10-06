# -*- coding: utf-8 -*-
from AccessControl.AuthEncoding import pw_encrypt
from AccessControl.AuthEncoding import pw_validate
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserChanger
from Products.membrane.interfaces import IMembraneUserObject
from dexterity.membrane import _
from dexterity.membrane.behavior.membraneuser import IMembraneUser
from dexterity.membrane.behavior.membraneuser import IMembraneUserWorkflow
from plone.directives import form
from z3c.form.interfaces import IAddForm
from zope import schema
from zope.component import adapter
from zope.component import queryUtility
from zope.interface import Invalid
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import invariant
from zope.interface import provider


class IPasswordChecker(Interface):
    """Check password strength or related
    """

    def check(password):
        """checks password if it is ok.

        returns False or an unicode/msgid why its wrong
        """


class IProvidePasswordsSchema(form.Schema):
    """Add password fields"""

    # Note that the passwords fields are not required; this means we
    # can add members without having to add passwords at that time.
    # The password reset tool should hopefully be able to deal with
    # that.

    password = schema.Password(
        title=_(u"Password"),
        required=False,
    )

    confirm_password = schema.Password(
        title=_(u"Confirm Password"),
        required=False,
    )

    @invariant
    def password_matches_confirmation(data):
        """password field must match confirm_password field.
        """
        password = getattr(data, 'password', None)
        confirm_password = getattr(data, 'confirm_password', None)
        if not password and not confirm_password:
            return
        if password != confirm_password:
            raise Invalid(_(u"The password and confirmation do not match."))
        pwchecker = queryUtility(IPasswordChecker)
        if not pwchecker:
            return
        result = pwchecker.check(password)
        if result:
            raise Invalid(result)


@provider(form.IFormFieldProvider)
class IProvidePasswords(IProvidePasswordsSchema):
    """Add password fields"""

    # Putting this in a separate fieldset for the moment:
    form.fieldset('membership', label=_(u"Membership"),
                  fields=['password', 'confirm_password'])

    form.omitted('password', 'confirm_password')
    form.no_omit(IAddForm, 'password', 'confirm_password')


@implementer(IProvidePasswordsSchema)
@adapter(IMembraneUser)
class PasswordProvider(object):

    def __init__(self, context):
        self.context = context

    @property
    def password(self):
        return getattr(self.context, 'password', None)

    @password.setter
    def _set_password(self, password):
        # When editing, the password field is empty in the browser; do
        # not do anything then.
        if password is not None:
            self.context.password = pw_encrypt(password)

    @property
    def confirm_password(self):
        # Just return the original password.
        return self._get_password()

    @confirm_password.setter
    def _set_confirm_password(self, confirm_password):
        # No need to store this.
        return


@adapter(IMembraneUser)
@implementer(IMembraneUserAuth)
class MembraneUserAuthentication(object):

    def __init__(self, context):
        self.context = context

    def verifyCredentials(self, credentials):
        """Returns True is password is authenticated, False if not.
        """
        user = IMembraneUserObject(self.context)
        if credentials.get('login') != user.getUserName():
            # Should never happen, as the code should then never end
            # up here, but better safe than sorry.
            return False
        if not IProvidePasswordsSchema.providedBy(self.context):
            return False
        return pw_validate(self.context.password,
                           credentials.get('password', ''))

    def authenticateCredentials(self, credentials):
        # Should not authenticate when the user is not enabled.
        workflow_info = IMembraneUserWorkflow(self.context)
        if not workflow_info.in_right_state():
            return
        if self.verifyCredentials(credentials):
            # return (self.getUserId(), self.getUserName())
            user = IMembraneUserObject(self.context)
            return (user.getUserId(), user.getUserName())


@adapter(IProvidePasswordsSchema)
@implementer(IMembraneUserChanger)
class MembraneUserPasswordChanger(object):
    """Supports resetting a member's password via the password reset form."""

    def __init__(self, context):
        self.context = context

    def doChangeUser(self, user_id, password, **kwargs):
        self.context.password = password
