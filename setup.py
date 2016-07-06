# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.1.1'

setup(
    name='dexterity.membrane',
    version=version,
    description="Dexterity content and behaviors to integrate with membrane.",
    long_description=(
        open("README.rst").read() + "\n" +
        open("CHANGES.rst").read()
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone dexterity membrane',
    author='Maurits van Rees',
    author_email='maurits@vanrees.org',
    url='https://github.com/collective/dexterity.membrane',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['dexterity'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFPlone>=4.2',
        'Products.membrane>=2.0.2',
        'bcrypt>=2.0',
        'collective.indexing>=2.0b1',
        'plone.app.dexterity',
        'plone.app.referenceablebehavior>=0.7.0',
        'setuptools',
        'zope.deprecation',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
