import unittest

#from zope.testing import doctestunit
import doctest
from zope.component import testing
#from Testing import ZopeTestCase as ztc

#from dexterity.membrane.tests import base


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctest.DocFileSuite(
        #    'README.txt', package='dexterity.membrane',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        doctest.DocTestSuite(
            module='dexterity.membrane.content.member',
            setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='dexterity.membrane',
        #    test_class=base.TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='dexterity.membrane',
        #    test_class=base.FunctionalTestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
