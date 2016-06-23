#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path as osp
import sys

from util import download_data


download_data(
    url='https://drive.google.com/uc?id=0B9P1L--7Wd2vMVNlR1JNV1RXLVE',
    md5='2da610302072f99ba7aa34ab145c4b0d',
    path='all.tgz',
    extract=True
)
