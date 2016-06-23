#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp

import numpy as np
from sklearn.cross_validation import train_test_split


def main():
    this_dir = osp.dirname(osp.realpath(__file__))
    dirs = os.listdir(osp.join(this_dir, 'all'))

    random_state = np.random.RandomState(1234)
    train_dirs, test_dirs = train_test_split(dirs, test_size=0.2,
                                             random_state=random_state)

    with open(osp.join(this_dir, 'train.txt'), 'w') as f:
        f.writelines((d + '\n' for d in train_dirs))
    with open(osp.join(this_dir, 'test.txt'), 'w') as f:
        f.writelines((d + '\n' for d in test_dirs))


if __name__ == '__main__':
    main()
