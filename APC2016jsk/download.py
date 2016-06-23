from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path as osp
import sys

this_dir = osp.dirname(osp.realpath(__file__))
sys.path.insert(0, osp.join(this_dir, '..'))
from util import download_data


download_data(
    url='https://drive.google.com/uc?id=0B9P1L--7Wd2vOU5WSWxvRzBGNEE',
    md5='a04dc13faea736e5ecf51488f6a4203c',
    path='2016-06-22-01-06-02.tgz',
    extract=True,
)
