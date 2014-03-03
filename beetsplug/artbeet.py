# -*- coding: utf-8 -*-
# Copyright (c) 2014, Berk Özbalcı
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import config
import artget
import sys
import os

class ArtbeetPlugin(BeetsPlugin):
   pass

def Procedure(artist, album, size, filename, autocorrect):
   fetcher = artget.Fetcher(artist, album, size, filename, autocorrect)
   try:
      fetcher.procedure()
   except artget.ArtgetError as e:
      sys.stderr.write("Artget error: %s\n" % e)
      sys.exit(1)

@ArtbeetPlugin.listen('album_imported')
def imported(lib=None, album=None):
   size = config['artbeet']['size'].get()
   filename = config['artbeet']['filename'].get()
   autocorrect = config['artbeet']['autocorrect'].get()

   try:
      Procedure(album['albumartist'], album['album'],
            size=size, filename=os.path.join(album.item_dir(), filename),
            autocorrect=autocorrect)
   except artget.ArtgetError as e:
      sys.stderr.write("artget: %s\n" % e)
   except Exception as e:
      sys.stderr.write("(artget) unhandled exception: %s\n" % e)
      sys.exit(1)
