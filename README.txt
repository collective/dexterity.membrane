Introduction
============

This is very much alpha code.  But it seems to work fine in a client
project.  Or at least the client where this package got copied from
seems to work fine.  It could be that too much client code has been
left behind here or removed, but it seems to be okay.


Compatibility
-------------

This package has been developed for Plone 4.1.  In fact it will only
work on that version (or higher) as we need uuid support.

We depend on Products.membrane 2.0.2 or higher as that contains a fix
to make sure members that are deleted are also removed from the
membrane_tool catalog.


User id
-------

As user id we use the uuid that is generated for the content item.
This only works on Plone 4.1 and higher.  See the definition of
``getUserId`` in the ``membraneuser.py`` behavior.

If you define your own member content type, you should enable the
``plone.app.referenceablebehavior.referenceable.IReferenceable``
behavior on it as that gives uuid support.  This also means members
can be referenced from Archetypes content.


Email as login name
-------------------

This package contains a member content type that has an email field.
This is used as login name by the behavior.  See ``getUserName``.
Other implementations are possible, so we do not force you to use the
email address as the login name in your site.  But setting the
use_email_as_login property to True is probably a good idea.  The only
effect this has as far as this package is concerned, is that some text
in login forms is changed: you see 'email address' as label instead of
'login name', mostly.  To enable this, you can put this in
``propertiestool.xml``, possibly in a custom package for your
project::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
    <object name="site_properties" meta_type="Plone Property Sheet">
      <property name="use_email_as_login" type="boolean">True</property>
    </object>
  </object>


Member content type
-------------------

This package defines a member content type, but this may be considered
an example; feel free to create a different type and only use the
behaviors or create your own adaptations of them.


Behaviors
---------

- ``dexterity.membrane.behavior.membraneuser.IMembraneUser``: this
  makes the content behave as a membrane user, defining a way to get
  the user id (``getUserId``) and login name (``getUserName``).

- ``dexterity.membrane.behavior.membraneuser.IProvidePasswords``:
  adds a password and confirmation field to your dexterity content.
  This is used during authentication.


Membrane implementation
-----------------------

- ``Products.membrane.interfaces.IMembraneUserAuth``: we implement
  authentication using the email field and the password field.

- ``Products.membrane.interfaces import IMembraneUserProperties``: we
  provide a read-only mapping from the first and last name fields of
  our own ``IMember`` schema to the fullname user property.  We have a
  read-write mapping for the email, home_page/homepage and
  description/bio properties/fields for ``IMember``.


Local roles
-----------

This package define a local role provider that makes sure a logged in
user gets the local Reader, Editor and Creator roles on the membrane
object that belongs to that user.


Workflow
--------

We define a simple workflow with pending/approved states.  A user can
only login when in the approved state.
