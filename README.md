artget
======

Fetch album arts from Last.fm, has MPD support.

Usage
=====


    usage: artget [-h] [-s SIZE] [-o OUTPUT] [-a ARTIST] [-b ALBUM] [-n HOSTNAME]
                  [-p PORT] [-r ROOT] [-N] [-A] [-t]
    
    Fetch album arts from Last.fm, has MPD support.
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SIZE, --size SIZE  between 1 and 5, pick size for image file (3)
      -o OUTPUT, --output OUTPUT
                            filename to save the downloaded album art
      -a ARTIST, --artist ARTIST
                            Look for this artist
      -b ALBUM, --album ALBUM
                            Look for this album
      -n HOSTNAME, --hostname HOSTNAME
                            specify hostname for the MPD server (localhost)
      -p PORT, --port PORT  specify port for the MPD server (6600)
      -r ROOT, --root ROOT  MPD music directory (useful with --to-music-dir
      -N, --no-autocorrect  do not use autocorrect by Last.fm
      -A, --album-artist    prefer albumartist tag on the current playing album
      -t, --to-music-dir    save album art to the music directory (only if it
                            exists)

If --artist and --album are specified, it will take priority over the
currently playing song.

If `--to-music-dir` is to be used with `--artist` and `--album` (so path to the music isn't known by MPD), the album art will be automatically placed into `mpd_root/artist/album/cover.jpg` where `mpd_root` is determined by the `--root` option and `artist/album` is determined by the options `--artist` and `--album`.

Examples
========

    artget --artist "Genesis" --album "Trespass" --size 5
    artget --port 3490 --no-autocorrect --album-artist
