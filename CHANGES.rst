Changelog
=========

0.5 (unreleased)
----------------

- Remove grok dependency, refactor a bit to reduce complexity in one module.
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
