import re

from plone.directives import form
from zope import schema
from zope.interface import Invalid, invariant

from z3c.form import group, field

from dexterity.membrane import _
from dexterity.membrane.membrane_helpers import validate_unique_email

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile


def is_email(value):
    """Is this an email address?

    We only do very basic validation, as the docs say we should just
    check if there is an '@' sign in the address.

    >>> is_email('joe@example.org')
    True
    >>> is_email('joe')
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email('')
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email(None)
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email(object())
    Traceback (most recent call last):
    ...
    Invalid: Not an email address

    """
    if not isinstance(value, basestring) or not '@' in value:
        raise Invalid(_(u"Not an email address"))
    return True


def is_url(value):
    """Is this a URL?

    >>> is_url("http://google.com/")
    True
    >>> is_url("https://google.com")
    True
    >>> is_url("http://example.org/folder/somepage")
    True
    >>> is_url("ssh://google.com")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("nothing")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(None)
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(object())
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link

    """
    if isinstance(value, basestring):
        pattern = re.compile(r"^https?://[^\s\r\n]+")
        if pattern.search(value.strip()):
            return True
    raise Invalid(_(u"Not a valid link"))


class IEmail(form.Schema):
    """Email address schema.

    If you have this field, we can make you a member.  To authenticate
    you also need a password though.
    """

    email = schema.TextLine(
        # String with validation in place looking for @, required.
        # Note that a person's email address will be their username.
        title=_(u"E-mail Address"),
        required=True,
        constraint=is_email,
        )

    @invariant
    def email_unique(data):
        """The email must be unique, as it is the login name (user name).

        The tricky thing is to make sure editing a user and keeping
        his email the same actually works.
        """
        user = data.__context__
        if user is not None:
            if hasattr(user, 'email') and user.email == data.email:
                # No change, fine.
                return
        error = validate_unique_email(data.email)
        if error:
            raise Invalid(error)


class IMember(IEmail,IImageScaleTraversable):
    """
    Member
    """




    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
        )
    
    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
        )    
    
    homepage = schema.TextLine(
        # url format
        title=_(u"External Homepage"),
        required=False,
        constraint=is_url,
        )   
    
    phone = schema.TextLine(
        title=_(u"Phone number"),
        required=True
    )
    
    form.fieldset('work',
            label=_(u"Work"),
            fields=['organization', 'sector','position', 'research_domain']
    )
    
    organization = schema.TextLine(
        title=_(u"Organization / Company"),
        required=True,
    )
    
    sector = schema.Choice(
        title=_(u"Sector"),
#        description=_(u"Where you are from"),
        required=False,
        vocabulary="dexterity.membrane.vocabulary.sector"

        )        

    position = schema.TextLine(
        title=_(u"Position / Role in Organization"),
        required=True,
    )     
        
    research_domain = schema.TextLine(

        title=_(u"research domain"),
        required=False,

        )
           
    form.fieldset('geography',
            label=_(u"Geography"),
            fields=['country', 'province','address']
    )
    
    country = schema.Choice(
        title=_(u"Country"),
        description=_(u"Where you are from"),
        required=False,
        vocabulary="collective.conference.vocabulary.countries"
    )

    province = schema.Choice(
        title=_(u"the province of your company"),
        vocabulary="dexterity.membrane.vocabulary.province",        
        required=True,
        ) 

    address = schema.TextLine(
        title=_(u"personal address"),       
        required=False,
        ) 
            
    bonus = schema.Int(
        # url format
        title=_(u"bonus"),
        required=False,
#        constraint=is_url,
        )    
    
    qq_number = schema.Int(
        # url format
        title=_(u"QQ Number"),
        required=False,

        )          

    form.widget(bio="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    bio = schema.Text(
        title=_(u"Biography"),
        required=False,
        )
    
    photo = NamedBlobImage(
        title=_(u"Photo"),
        description=_(u"Your photo or avatar. Recommended size is 150x195"),
        required=False
    )
    
    form.omitted('bonus')        
