# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '3.0.2'

setup(
    name='dexterity.membrane',
    version=version,
    description='Dexterity content and behaviors to integrate with membrane.',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone :: Addon',
        'Framework :: Plone :: 5.2',
        'Framework :: Plone :: 6.0',
        'Framework :: Plone',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
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
    python_requires=">=3.6",
    install_requires=[
        'Products.CMFPlone>=5.2',
        'Products.membrane',
        'bcrypt>=2.0',
        'plone.api',
        'plone.app.dexterity',
        'plone.memoize',
        'setuptools',
        'zope.deprecation',
    ],
    extras_require={
        'archetypes': [
            'plone.app.referenceablebehavior>=0.7.0',
        ],
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
