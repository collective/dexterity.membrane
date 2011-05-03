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

If you define your own member content type, you should enable the the
plone.app.referenceablebehavior.referenceable.IReferenceable on it as
that gives uuid support.  This also means members can be referenced
from Archetypes content.


Email as login name
-------------------

This package contains a member content type that has an email field.
This is used as login name by the behavior.  See ``getUserName``.
Other implementations are possible.  Putting this in
``propertiestool.xml`` would be a good idea, possibly in a custom
package for you project::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
    <object name="site_properties" meta_type="Plone Property Sheet">
      <property name="use_email_as_login" type="boolean">True</property>
    </object>
  </object>


Behaviors
---------


Member content type
-------------------

This may be considered an example; feel free to create a different
type and only use the behaviors.
