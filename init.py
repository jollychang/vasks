#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath, join
INITPATH = dirname(abspath(__file__))
VASKSPATH = dirname(INITPATH)
if VASKSPATH not in sys.path:
    sys.path.insert(0, VASKSPATH)
if INITPATH not in sys.path:
    sys.path.insert(0, INITPATH)
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=join(INITPATH, 'vasks.log'),
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s:  %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)
