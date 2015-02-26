dexterity.membrane Installation
-------------------------------

Using zc.buildout and the plone.recipe.zope2instance recipe to manage your project, do this:

* Add ``dexterity.membrane`` to the list of eggs to install, e.g.:

    [buildout]
    ...

    [instance]
    recipe = plone.recipe.zope2instance
    ...

    eggs =
        ...
        dexterity.membrane

* Re-run buildout, e.g. with:

    $ ./bin/buildout

Now start the instance and activate the add on in the plone control-panel.
