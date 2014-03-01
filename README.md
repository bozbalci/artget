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

    usage: artget [-h] [-s {1,2,3,4,5}] [-o OUTPUT] [-a ARTIST] [-b ALBUM]
                  [-n HOSTNAME] [-p PORT] [-P PASSWORD] [-r ROOT] [-N] [-A] [-t]
    
    Fetch album arts from Last.fm, has MPD support.
    
    optional arguments:
      -h, --help            show this help message and exit
      -s {1,2,3,4,5}, --size {1,2,3,4,5}
                            between 1 and 5, pick size for image file (default: 3)
      -o OUTPUT, --output OUTPUT
                            filename to save the downloaded album art (default:
                            cover.jpg)
      -a ARTIST, --artist ARTIST
                            Look for this artist (default: None)
      -b ALBUM, --album ALBUM
                            Look for this album (default: None)
      -n HOSTNAME, --hostname HOSTNAME
                            specify hostname for the MPD server (default:
                            localhost)
      -p PORT, --port PORT  specify port for the MPD server (default: 6600)
      -P PASSWORD, --password PASSWORD
                            specify password for the MPD server (default: None)
      -r ROOT, --root ROOT  MPD music directory (useful with --to-music-dir)
                            (default: ~/music/)
      -N, --no-autocorrect  do not use autocorrect by Last.fm (default: True)
      -A, --album-artist    prefer albumartist tag on the current playing album
                            (default: False)
      -t, --to-music-dir    save album art to the music directory (only if it
                            exists) (default: False)

If `--artist` and `--album` are specified, it will take priority over the
currently playing song.

If `--to-music-dir` is to be used with `--artist` and `--album` (so path to the music isn't known by MPD), the album art will be automatically placed into `mpd_root/artist/album/cover.jpg` where `mpd_root` is determined by the `--root` option and `artist/album` is determined by the options `--artist` and `--album`.

Examples
========

    artget -t --size=5 -a "Miles Davis" -b "Bitches Brew" -o front.jpg
    artget --artist "Genesis" --album "Trespass" --size 5
    artget --port 3490 --no-autocorrect --album-artist

TODO
====

* Write a basic shell script to invoke artget on every new album on music library (might make that a beets plugin aswell)
* Add a non-download option which only provides the link to the output.
