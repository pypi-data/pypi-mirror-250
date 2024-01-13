#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/chatopera/efaqa-corpus-raw/efaqa_corpus_raw/exporter.py
# Author: Hai Liang Wang
# Date: 2024-01-06:09:28:07
#
#===============================================================================

"""
   
"""
__copyright__ = "Copyright (c) 2024 Chatopera Inc. <https://www.chatopera.com/> All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2024-01-06:09:28:07"

import os, sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()
import json

CORPUS_FILE_PATH = os.path.join(curdir, "data", "efaqa_corpus_raw.utf8.gz")


def load():
    '''
    Load corpus data from disk, download corpus if not present.
    '''
    pass