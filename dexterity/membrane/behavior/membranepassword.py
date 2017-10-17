# -*- coding: utf-8 -*-
from password import IProvidePasswords as BBBIProvidePasswords
from password import IProvidePasswordsSchema as BBBIProvidePasswordsSchema


class IProvidePasswordsSchema(BBBIProvidePasswordsSchema):
    """ BBB class for zc.relations stuff and other weirdness """


class IProvidePasswords(BBBIProvidePasswords):
    """ BBB class for zc.relations stuff and other weirdness """
