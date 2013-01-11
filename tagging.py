# Metadata tag support for whatbetter.
#
# Copyright (c) 2013 Milky Joe <milkiejoe@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Simple tagging for whatbetter.
"""

import os.path
import mutagen.flac
import mutagen.mp3
from mutagen.easyid3 import EasyID3

class TaggingException(Exception):
    pass

def copy_tags(flac_file, transcode_file):
    flac_info = mutagen.flac.FLAC(flac_file)
    transcode_info = None
    valid_key_fn = None
    ext = os.path.splitext(transcode_file)[1]

    if ext == '.flac':
        transcode_info = mutagen.flac.FLAC(transcode_file)
        valid_key_fn = lambda k: True

    elif ext == '.mp3':
        transcode_info = mutagen.mp3.EasyMP3(transcode_file)
        valid_key_fn = lambda k: k in EasyID3.valid_keys.keys()

    else:
        raise TaggingException('Unsupported tag format "%s"' % transcode_file)

    for tag in filter(valid_key_fn, flac_info):
        transcode_info[tag] = flac_info[tag]
    transcode_info.save()

# EasyID3 extensions for whatbetter.

for key, frameid in {
    'albumartist': 'TPE2',
    'album artist': 'TPE2',
    'grouping': 'TIT1',
    'content group': 'TIT1',
    }.iteritems():
    EasyID3.RegisterTextKey(key, frameid)

def comment_get(id3, _):
    return [comment.text for comment in id3['COMM'].text]

def comment_set(id3, _, value):
    id3.add(mutagen.id3.COMM(encoding=3, lang='eng', desc='', text=value))

def originaldate_get(id3, _):
    return [stamp.text for stamp in id3['TDOR'].text]

def originaldate_set(id3, _, value):
    id3.add(mutagen.id3.TDOR(encoding=3, text=value))

EasyID3.RegisterKey('comment', comment_get, comment_set)
EasyID3.RegisterKey('description', comment_get, comment_set)
EasyID3.RegisterKey('originaldate', originaldate_get, originaldate_set)
EasyID3.RegisterKey('original release date', originaldate_get, originaldate_set)
