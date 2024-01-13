#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2024 Chatopera Inc. <https://www.chatopera.com> All Rights Reserved
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
__all__ = ["corpus"]

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
from chatoperastore import download_licensedfile

try:
    from smart_open import smart_open
except ImportError:
    print("smart_open library not found; falling back to local-filesystem-only")

    def make_closing(base, **attrs):
        """
        Add support for `with Base(attrs) as fout:` to the base class if it's missing.
        The base class' `close()` method will be called on context exit, to always close the file properly.

        This is needed for gzip.GzipFile, bz2.BZ2File etc in older Pythons (<=2.6), which otherwise
        raise "AttributeError: GzipFile instance has no attribute '__exit__'".

        """
        if not hasattr(base, '__enter__'):
            attrs['__enter__'] = lambda self: self
        if not hasattr(base, '__exit__'):
            attrs['__exit__'] = lambda self, type, value, traceback: self.close()
        return type('Closing' + base.__name__, (base, object), attrs)

    def smart_open(fname, mode='rb'):
        _, ext = os.path.splitext(fname)
        if ext == '.bz2':
            from bz2 import BZ2File
            return make_closing(BZ2File)(fname, mode)
        if ext == '.gz':
            from gzip import GzipFile
            return make_closing(GzipFile)(fname, mode)
        return open(fname, mode)


EFAQA_RAW_LICENSE = os.environ.get("EFAQA_RAW_LICENSE", None)
CORPUS_FILE_PATH = os.path.join(curdir, "data", "efaqa_corpus_raw.utf8.gz")
corpus = None

def download(to_file):
    '''
    Download corpus from chatopera store
    '''
    download_licensedfile(EFAQA_RAW_LICENSE, to_file)

def load():
    '''
    Load corpus data from disk, download corpus if not present.
    '''
    if not os.path.exists(CORPUS_FILE_PATH):
        # Download corpus
        download(CORPUS_FILE_PATH)

    # read data
    try:
        with smart_open(CORPUS_FILE_PATH) as f:
            for x in f:
                yield json.loads(x)
    except BaseException as e:
        print(e)
        raise e

corpus = list(load())
print("[Emotional First Aid Raw Dataset] Loaded conversation size: %s" % len(corpus))