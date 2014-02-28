artget
======

Fetch album arts from Last.fm, has MPD support.

Usage
=====

    usage: artget [-h] [--size SIZE] [--output OUTPUT] [--artist ARTIST]
                  [--album ALBUM] [--hostname HOSTNAME] [--port PORT]
                  [--root ROOT] [--no-autocorrect] [--album-artist]
                  [--to-music-dir]
    
    Fetch album arts from Last.fm, has MPD support.
    
    optional arguments:
      -h, --help           show this help message and exit
      --size SIZE          between 1 and 5, pick size for image file (3)
      --output OUTPUT      filename to save the downloaded album art
      --artist ARTIST      Look for this artist
      --album ALBUM        Look for this album
      --hostname HOSTNAME  specify hostname for the MPD server (localhost)
      --port PORT          specify port for the MPD server (6600)
      --root ROOT          MPD music directory (useful with --to-music-dir
      --no-autocorrect     do not use autocorrect by Last.fm
      --album-artist       prefer albumartist tag on the current playing album
      --to-music-dir       save album art to the music directory (only if it
                           exists)
    
    If --artist and --album are specified, it will take priority over the
    currently playing song.

If `--to-music-dir` is to be used with `--artist` and `--album` (so path to the music isn't known by MPD), the album art will be automatically placed into `mpd_root/artist/album/cover.jpg` where `mpd_root` is determined by the `--root` option and `artist/album` is determined by the options `--artist` and `--album`.

Examples
========

    artget --artist "Genesis" --album "Trespass" --size 5
    artget --port 3490 --no-autocorrect --album-artist
