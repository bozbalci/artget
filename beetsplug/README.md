artbeet
=======

[beets](https://github.com/sampsyo/beets) plugin for [artget](https://github.com/berkoz/artget), album art grabber

It will grab the album art for the current album being imported by beets. Since the fetchart plugin hasn't been able to grab the artwork for most of the albums in my library, I wrote this plugin to make my life easier. Hope this helps you, too.

Installation
============

Put the file `artbeet.py` into your beet plugins directory.

Requirements
============
* Tested on Python 2.7.6
* [artget](https://github.com/berkoz/artget)
* [beets](https://github.com/sampsyo/beets)

Configuration
=============

For artbeet to work properly, open your beets' `config.yaml` file and append to the line

    plugins: [ ... ] artbeet

Open a section for artbeet like the following:

    artbeet:
      size: 4
      autocorrect: yes
      filename: cover.jpg

All of these options must be present or artbeet will not function properly. The options listed above are analogous to the arguments passed to the program artget.
