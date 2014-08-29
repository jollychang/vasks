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

from jenkins import get_scm_dict_by_view, \
                    format_port_list, \
                    reuse_port

un_format_ports = [20110, 40410, 40420, 20100, 20120, 20130, 20940, 40000, 40200, 40400, 50001]
format_ports = [20100, 20110, 20120, 20130, 20940, 40000, 40200, 40400, 40410, 40420]

class JenkinsTest(TestCase):

    def test_format_port_list(self):
        self.assertEqual(format_port_list(un_format_ports), format_ports)

    def test_reuse_port(self):
        self.assertEqual(reuse_port(format_ports), 20140)
        self.assertEqual(reuse_port([10100, 10110]), 'no port can be reuse,you need a new port')
        self.assertEqual(reuse_port([]), 'no port can be reuse,you need a new port')
        self.assertEqual(reuse_port([10100]), 'no port can be reuse,you need a new port')

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
