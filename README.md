artget
======

Fetch album arts from Last.fm, has MPD support.

Usage
=====

    usage: artget [-h] [--size SIZE] [--output OUTPUT] [--artist ARTIST]
                  [--album ALBUM] [--hostname HOSTNAME] [--port PORT]
                  [--no-autocorrect] [--album-artist]
    
    Fetch album arts from Last.fm, has MPD support.
    
    optional arguments:
      -h, --help           show this help message and exit
      --size SIZE          between 1 and 5, pick size for image file (3)
      --output OUTPUT      filename to save the downloaded album art
      --artist ARTIST      Look for this artist
      --album ALBUM        Look for this album
      --hostname HOSTNAME  specify hostname for the MPD server (localhost)
      --port PORT          specify port for the MPD server (6600)
      --no-autocorrect     do not use autocorrect by Last.fm
      --album-artist       prefer albumartist tag on the current playing album
    
    If --artist and --album are specified, it will take priority over the
    currently playing song.

Examples
========

    artget --artist "Genesis" --album "Trespass" --size 5
    artget --port 3490 --no-autocorrect --album-artist
