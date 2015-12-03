#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import argparse
import os
import podpublish
import sys
from podpublish import configuration
from podpublish import uploader

def main():
    parser = argparse.ArgumentParser(description='Publish a podcast, previously encoded with encode_podcast, to sftp and YouTube.')
    parser.add_argument('--version', action='version', version=podpublish.__version__)
    parser.add_argument('filename', type=argparse.FileType('r'), help="Podcast configuration file.")
    args = parser.parse_args()

    config = configuration.Configuration(args.filename)

    if not config.skip_mp3 and not config.skip_sftp:
        if os.path.isfile(config.mp3_file):
            uploader.sftp_upload(config, config.mp3_file)
        else:
            print('ERROR! ' + config.mp3_file + ' is missing. Abort.')
            sys.exit(1)

    if not config.skip_mp3 and not config.skip_sftp:
        if os.path.isfile(config.ogg_file):
            uploader.sftp_upload(config, config.ogg_file)
        else:
            print('ERROR! ' + config.ogg_file + ' is missing. Abort.')
            sys.exit(1)

    if not config.skip_wordpress:
        uploader.wordpress_post(config)

    if not config.skip_youtube:
        if os.path.isfile(config.mkv_file):
            uploader.youtube_upload(config)
        else:
            print('ERROR! ' + config.mkv_file + ' is missing. Abort.')
            sys.exit(1)

if __name__ == '__main__':
    main()
