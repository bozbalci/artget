artget
======

Fetch album arts from Last.fm, has MPD support.

Requirements
============
* Tested on Python 2.7.6
* [requests](http://requests.readthedocs.org/en/latest/)
* [python-mpd2](https://github.com/Mic92/python-mpd2)

Usage
=====

    usage: artget [options]
    
    Fetch album arts from Last.fm, has MPD support.
    
    optional arguments:
      -h, --help      show this help message and exit
      -s {1,2,3,4,5}  size for album art
      -o OUTPUT       filename to save the album art
      -N              do not use autocorrect by Last.fm
      -a ARTIST       look for this artist
      -b ALBUM        look for this album
      -n HOST         MPD host
      -p PORT         MPD port
      -P PASSWORD     MPD password
      -r ROOT         MPD music directory (useful with -t)
      -A              prefer albumartist tag on the current playing album
      -t              save album art to the music directory
    
    If -a and -b are specified, they will take priority over MPD.

See the beetsplug directory for [beets](https://github.com/sampsyo/beets) plugin.

Examples
========

    artget -t -s 4 -a "Miles Davis" -b "Bitches Brew" -o front.jpg
