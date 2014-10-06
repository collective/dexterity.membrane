# -*- coding: utf-8 -*-
from dexterity.membrane.testing import DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING
from plone.testing import layered
import doctest
import unittest

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

testfiles = [
]


def test_suite():
    suite = unittest.TestSuite()
    for testfile in testfiles:
        suite.addTest(
            layered(
                doctest.DocFileSuite(
                    testfile,
                    package='dexterity.membrane'
                ),
                layer=DEXTERITY_MEMBRANE_FUNCTIONAL_TESTING
            )
        )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
