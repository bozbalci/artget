#!/usr/bin/env python
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

import sys
import os
import argparse

from mpd import MPDClient, MPDError, CommandError
import requests

VERSION = (0, 1, 0)
API_URL = "http://ws.audioscrobbler.com"
API_KEY = "a76e4f3f6a9e81f45a943509437a125f"

class ArtgetError(Exception):
   """ Fatal error in artget. """

class Fetcher:
   def __init__(self, artist, album, size, path, autocorrect):
      self.size = size
      self.path = path
      self.payload = { 'api_key': API_KEY, 'artist': artist, 'album': album,
            'autocorrect': int(autocorrect), 'format': 'json' }

   def find_album(self):
      try:
         r = requests.get(API_URL + '/2.0/?method=album.getinfo', params=self.payload)
      except (requests.ConnectionError, requests.Timeout) as e:
         raise ArtgetError("There was an error making a request to Last.fm: %s" %
               e)

      albuminfo = r.json()

      try:
         albuminfo['album']
      except KeyError:
         raise ArtgetError("This album doesn't seem to exist on Last.fm")
      self.albuminfo = albuminfo['album']

   def find_image(self):
      try:
         self.albuminfo
      except NameError:
         raise ArtgetError("The album hasn't been found yet.")

      images = self.albuminfo['image']
      count = len(images)

      if count == 0:
         raise ArtgetError("This album doesn't seem to have album art on Last.fm")

      # Take nearest item the list. Not every album may have images of all sizes
      i = min(range(1, count + 1), key=lambda x: abs(x - self.size))

      # This is the URL.
      url = images[i - 1]['#text']

      if url == '':
         raise ArtgetError("This album doesn't seem to have album art on Last.fm")
      self.url = url

   def download_image(self):
      try:
         with open(self.path, 'wb') as fd:
            try:
               r = requests.get(self.url, stream = True)
            except (requests.ConnectionError, requests.Timeout) as e:
               raise ArtgetError("There was an error downloading the album art: %s" %
                     e)
            for block in r.iter_content(1024):
               if not block:
                  break
               fd.write(block)
      except IOError as err:
         errno, errstr = err
         raise ArtgetError("Could not write to file: %s" % errstr)

   def procedure(self):
      self.find_album()
      self.find_image()
      self.download_image()

class MPDConnection:
   def __init__(self, host, port, password=None, use_unicode=True):
      self.host = host
      self.port = port
      self.password = password
      self.use_unicode = use_unicode
      self.connected = False
      self.client = MPDClient(use_unicode)

   def connect(self):
      # If already connected, just reconnect
      if self.connected:
         self.disconnect()
         self.connect()

      try:
         self.client.connect(self.host, self.port)
      except IOError as err:
         errno, errstr = err
         raise ArtgetError("Could not connect to '%s' : %s" %
               (self.host, errstr))
      except MPDError as e:
         raise ArtgetError("Could not connect to '%s' : %s" %
               (self.host, e))
      if self.password:
         try:
            self.client.password(self.password)
         except CommandError as e:
            raise ArtgetError("Could not connect to '%s' : "
                  "password command failed: %s" %
                  (self.host, e))
         except (MPDError, IOError) as e:
            raise ArtgetError("Could not connect to '%s' : "
                  "password command failed: %s" %
                  (self.host, e))

      self.connected = True
   
   def disconnect(self):
      # Don't go further if there's no connection
      if not self.connected:
         return

      try:
         self.client.close()
      except (MPDError, IOError):
         # Don't worry, just ignore it, disconnect
         pass
      try:
         self.client.disconnect()
      except (MPDError, IOError):
         # Now this is serious. This should never happen.
         # The client object should not be trusted to be re-used.
         self.client = MPDClient(self.use_unicode)

      self.connected = False

   def current_song(self):
      try:
         song = self.client.currentsong()
      except (MPDError, IOError):
         # Try reconnecting and retrying
         self.disconnect()
         try:
            self.connect()
         except ArtgetError as e:
            raise ArtgetError("Reconnecting failed: %s" % e)
         try:
            song = self.client.currentsong()
         except (MPDError, IOError) as e:
            # Failed again, just give up.
            raise ArtgetError("Couldn't retrieve current song: %s" % e)
      if song == {}:
         raise ArtgetError("No song is playing on MPD")
      self.song = song

   def procedure(self):
      self.connect()
      self.current_song()
      self.disconnect()

def parse_args():
   parser = argparse.ArgumentParser(prog='artget',
         description='Fetch album arts from Last.fm, has MPD support.',
         epilog='If -a and -b are specified, they will take priority over MPD.',
         usage='%(prog)s [options]')

   parser.add_argument('-s', type=int, choices=range(1,6), dest='size',
         help='size for album art')
   parser.add_argument('-o', type=str, dest='output',
         help='filename to save the album art')
   parser.add_argument('-N', action='store_false', dest='autocorrect',
         help='do not use autocorrect by Last.fm')
   parser.add_argument('-a', type=str, dest='artist', help='look for this artist')
   parser.add_argument('-b', type=str, dest='album', help='look for this album')
   parser.add_argument('-n', type=str, dest='host', help='MPD host')
   parser.add_argument('-p', type=int, dest='port', help='MPD port')
   parser.add_argument('-P', type=str, dest='password', help='MPD password')
   parser.add_argument('-r', type=str, dest='root',
         help='MPD music directory (useful with -t)')
   parser.add_argument('-A', action='store_true', dest='albumartist',
         help='prefer albumartist tag on the current playing album')
   parser.add_argument('-t', action='store_true', dest='tomusicdir',
         help='save album art to the music directory')

   parser.set_defaults(size=3, output='cover.jpg', host='localhost', port=6600,
         root='~/music/')
   args = parser.parse_args()
   return args

def main():
   args = parse_args()
   
   # This is to be played around with.
   output = args.output

   # Check if both --artist and --album exists
   if (args.artist and not args.album) or (args.album and not args.artist):
      raise ArtgetError("Both artist and album must be specified")

   # Grab from command-line args
   if (args.artist and args.album):
      artist = args.artist
      album = args.album

      # Assume the ideal organisation of the music directory and place the
      # downloaded art there. This is especially useful for people who use
      # the awesome piece of software called beets.
      if args.tomusicdir:
         # I removed this feature because it isn't useful for most people, and there
         # is a really high probability of missing the correct directory (album titles
         # start with a dot, accented characters aren't in the name, etc.) You may
         # re-enable it back, but I wouldn't recommend this.

         # output = os.path.join(os.path.expanduser(args.root),
         #       artist, album, args.output)
         raise ArtgetError("-t cannot be used together with -a and -b.")
   else:
      # Grab from MPD
      client = MPDConnection(args.host, args.port, args.password, True)
      client.procedure()

      artist = client.song['artist']
      if args.albumartist:
         artist = client.song['albumartist']

      album = client.song['album']

      # Locate the song playing on MPD and write to there
      if args.tomusicdir:
         output = os.path.join(os.path.expanduser(args.root),
               os.path.dirname(client.song['file']), args.output)

   if any([a == '' for a in [album, artist]]):
         raise ArtgetError("Artist or album could not be determined.")

   # Do the work, and bail out. :)
   fetcher = Fetcher(artist, album, args.size, output, args.autocorrect)
   fetcher.procedure()

if __name__ == '__main__':
   try:
      main()
   except ArtgetError as e:
      sys.stderr.write("Error: %s\n" % e)
      sys.exit(1)
   except Exception as e:
      sys.stderr.write("Unexpected exception: %s\n" % e)
      sys.exit(1)
   except:
      sys.exit(0)
