Changelog
=========


3.0.1 (2023-03-24)
------------------

- Fix for `AuthEncoding >= 5.0`.
  [petschki]

- Rename profile `dexterity.membrane: example` -> `dexterity.membrane: content`
  and add uninstall profile for it.
  [petschki]

- Remove py2.7 and Plone < 5.2 support.
  [petschki]

- Warning: The package is not tested anymore on Plone 5.2 and Python 3.6
  because Plone 5.2 is not tested as well on that Python version.


3.0.0 (2021-12-06)
------------------

- remove `<includeDependencies />`
  [petschki]


3.0.0a2 (2020-11-30)
--------------------

- Performance improvements: cache expensive bcrypt operations
  [ale-rt]


3.0.0a1 (2020-02-19)
--------------------

- Plone5.2 porting: do not require Archetypes
  [ale-rt]

- ZCML namespace cleanup.
  [thet]

- Added uninstall profile
  [agitator]


2.1.0 (2019-06-01)
------------------

- Depend on plone.api
  [ale-rt]
- Fixed some docstring
  [ale-rt]
- Biography: plone.app.textfield RichText field for Plone 5
  [ksuess]
- Fix AttributeError: 'tuple' object has no attribute 'strip'
  [b4oshany]


2.0.1 (2018-01-18)
------------------

- Performance improvements: cache expensive bcrypt operations
  [ale-rt]


2.0 (2017-10-21)
----------------

- Removed collective.indexing dependency. Collective.indexing was merged into Plone 5.1
  If you're using this package with a Plone version < than 5.1, please add collective.indexing manually and pin Products.membrane to < 4.
  [agitator]

- Dropping official support for Plone < 4.3, use 1.2.x for older versions of Plone.
  [agitator]


1.2 (2017-01-11)
----------------

- No longer officially support Python 2.6.  See compatibility in readme.
  [maurits]

- Enable use_email_as_username without use_uuid_as_userid.
  This fixes getUserId, which fixes the indexed user values,
  which fixes enumerateUsers.
  Warning: if you already have members and you change the settings,
  this may need reindexing, or editing and saving all users manually.
  Fixes https://github.com/collective/dexterity.membrane/issues/26
  [gyst]


1.1.2 (2016-08-05)
------------------

- Added backwards compatibility import for ``membranepasswords.IProvidePasswords``.
  Otherwise z3c.relationfield may give problems when editing content.
  Fixes https://github.com/collective/dexterity.membrane/issues/23
  [mikejmets]


1.1.1 (2016-07-06)
------------------

- A group might accidentally show up as a user.
  ``portal_membership.listMembers`` then says: ``AttributeError:
  'NoneType' object has no attribute '__of__'``.  We prevent this by
  implementing getUserId and getUserName on groups, returning the
  group id and group name.  [maurits]


1.1.0 (2015-10-07)
------------------

- Switch to bcrypt encryption for passwords
  (includes backwards-compatibility with existing SSHA passwords)
  [mgrbyte]


1.1.0b2 (2015-03-03)
--------------------

- added BBB class for IMembraneGroup, IProvidePasswordsSchema and IMembraneUser
  [agitator]


1.1.0b1 (2015-03-02)
--------------------

- fix release


1.1.0b0 (2015-03-02)
--------------------

- support special characters/umlauts in passwords
  [agitator]

- renaming with bbb imports: remove last ``membrane`` from all
  ``dexterity.membrane.behavior.membrane*``.
  [jensens]

- fix: make ``PasswordProvider`` work. The whole was inactive and broken after
  activation.
  [jensens]

- Get rid of deprecated plone.directives and use plone core functionality to
  achieve same goals. Also minor modernization of buildout.
  [jensens]

- Declare plone.directives.form dependency.
  [vincentfretin]


1.0 (2014-10-16)
----------------

- add a hook using a utility to add a password checker in own customization
  code. we may want to provide an default, but yet not sure how it should
  look like.
  [jensens]

- make it easier to inherit passowrd for own behavior
  [jensens]

- Remove grok dependency, refactor a bit to reduce complexity in one module.
  Attention: password related behaviour is now in own module. Needs update of
  customizations/own code after upgrade.
  [jensens]

- Cleanup, pep8, plone-code-style, make tests fly again.
  [jensens]

- Make get_full_name a method of MembraneUser so it can be easily customized.
  [cedricmessiant, vincentfretin]

- Add French translations.
  [cedricmessiant]

0.4 (2013-07-18)
----------------

- Add upgrade step to update the behavior profile.  If you have
  installed the example content profile, you will see a warning in the
  Add-ons control panel that Plone does not know how to update this
  profile.  We recommend that you deactivate it and then activate it
  again.  Issue #7
  [maurits]

- Rename content profile to example and rename behavior profile to
  default.  Issue #7.
  [maurits]

- Add Spanish and Brazilian Portuguese translations. [hvelarde]


0.3 (2013-05-15)
----------------

- Fix installation problems when OS does not support symbolic links. Renamed
  ``README.txt`` to ``README.rst`` and updated ``setup.py`` to point to that
  file. This fixes #5.
  [saily]

- Fix getattr in getPropertiesForUser to have a default value.
  [datakurre]


0.2 (2013-02-19)
----------------

- Keep constistent with plone's email login #12187, so don't lowercase email
  addresses.
  [saily]

- Add basic membrane group behavior
  [saily]


0.1 (2012-09-20)
----------------

- Initial alpha release
