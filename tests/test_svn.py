#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from unittest2  import TestCase
from os.path import dirname, abspath


INITPATH = dirname(abspath(__file__))
VASKSPATH = dirname(INITPATH)
if VASKSPATH not in sys.path:
    sys.path.insert(0, VASKSPATH)
if INITPATH not in sys.path:
    sys.path.insert(0, INITPATH)

from config import SVN_ROOT_URL
from svn import get_svn_branches_list, get_branch_url_by_file_list, get_branch_url_from_svn

class SvnTest(TestCase):

    def test_get_branch_url_by_file_list(self):
        input = "%s/branches/test1/d1/d2/d3/f1.py" % SVN_ROOT_URL
        output = "%s/branches/test1/d1/" % SVN_ROOT_URL
        self.assertEqual(get_branch_url_by_file_list(input, 3), output)

    def test_get_branch_url_from_svn(self):
        input1 = "%s/branches/test1/view/__init__.py" % SVN_ROOT_URL
        input2 = "%s/branches/test-2/song.py"
        output2 = "%s/branches/test-3/" % SVN_ROOT_URL
        self.assertEqual(get_branch_url_from_svn(input1), "non-existent shire branch")
        self.assertEqual(get_branch_url_from_svn(input2), output2)
        self.assertEqual(get_branch_url_from_svn(input2), output2)



if __name__ == '__main__':
    # junit xml report for jenkins
    import sys
    if len(sys.argv) > 1 and sys.argv[-1] == '--junit-xml':
        try:
            import xmlrunner
        except ImportError:
            print >> sys.stderr, 'Please: pip install unittest-xml-reporting'
            sys.exit(1)
        runner = xmlrunner.XMLTestRunner(output='test-reports')
        del sys.argv[-1]
    else:
        runner = None

    import unittest2
    unittest2.main(testRunner=runner)