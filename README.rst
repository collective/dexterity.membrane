Introduction
============

dexterity.membrane enables dexterity content items to be used as users and groups in Plone sites and integrates with Products.membrane.

.. image:: https://travis-ci.org/collective/dexterity.membrane.png
    :target: https://travis-ci.org/collective/dexterity.membrane


Compatibility
-------------

This package is currently tested and developed for Plone 5.1+.

With Plone 5.2+, Products.membrane 5 or higher is needed.

We depend on Products.membrane 4 higher as that contains a fix to make sure members that are deleted are also removed from the membrane_tool catalog.

When using Python2.7 you will need to pin bcrypt to the latest compatible version::

    [versions:python27]
    bcrypt = 3.1.7


User id
-------

As user id we use the uuid that is generated for the content item.
This only works on Plone 4.1 and higher.
See the definition of ``getUserId`` in the ``user.py`` behavior.

This also means members can be referenced from Archetypes content.


Note for archetype users
------------------------

If you define your own member content type, you should enable the ``plone.app.referenceablebehavior.referenceable.IReferenceable`` behavior on it as that gives uuid support.


Email as login name
-------------------

This package contains a member content type that has an email field.
This is used as login name by the behavior.
See ``getUserName``.
Other implementations are possible, so we do not force you to use the email address as the login name in your site.

By default, this is on, but you can switch it off in our control panel.
The setting is saved in the Plone registry.

Aside from this, it is probably a good idea to also switch on the use_email_as_login property of Plone itself.
The only effect this has as far as this package is concerned, is that some text in login forms is changed:
you see ``email address`` as label instead of ``login name``, mostly.
To enable this, you can put this in ``propertiestool.xml`` (Plone 4), possibly in a custom package for your project::

  <?xml version="1.0"?>
  <object name="portal_properties" meta_type="Plone Properties Tool">
    <object name="site_properties" meta_type="Plone Property Sheet">
      <property name="use_email_as_login" type="boolean">True</property>
    </object>
  </object>


Warning about changing settings
-------------------------------

It is best to configure the settings once, and then not touch them anymore.
If you change the settings when you already have created members, some reindexing may be needed.
If there are just a few members, editing and saving them all will be the easiest way.
If you have dozens or hundreds of members this is not very practical.
Future versions might automate this.
If you are interested in helping, a `pull request <https://github.com/collective/dexterity.membrane/pulls>`_ would be nice.


Member content type
-------------------

This package defines a member content type, but this may be considered an example;
feel free to create a different type and only use the behaviors or create your own adaptations of them.


Behaviors
---------

``dexterity.membrane.user``
    this makes the content behave as a membrane user, defining a way to get the user id (``getUserId``) and login name (``getUserName``).

``dexterity.membrane.provide_password``
    adds a password and confirmation field to your dexterity content.
    This is used during authentication.

``dexterity.membrane.group``
    this makes the content behave as a membrane group, defining a way to get the group id (``getGroupId``) and group name (``getGroupName``).

``dexterity.membrane.name_from_fullname``
    use member fullname to make the object id


Membrane implementation
-----------------------

``Products.membrane.interfaces.IMembraneUserAuth``
    we implement authentication using the email field and the password field.

``Products.membrane.interfaces import IMembraneUserProperties``
    we provide a read-only mapping from the first and last name fields of our own ``IMember`` schema to the fullname user property.
    We have a read-write mapping for the email, home_page/homepage and description/bio properties/fields for ``IMember``.


Local roles
-----------

This package defines a local role provider.
It makes sure a logged in user gets the local Reader, Editor and Creator roles on the membrane object that belongs to that user.


Workflow
--------

We define a simple workflow with pending/approved states.
A user can only login when in the approved state.


Encryption
----------

As of 1.1.0b3, dexterity.membrane uses bcrypt_ to encrypt new passwords.
This change maintains support for existing SSHA passwords.

.. _bcrypt: https://en.wikipedia.org/wiki/Bcrypt
