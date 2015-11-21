#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

from podpublish import configuration
from podpublish import encoder
from podpublish import uploader

def main():
    config = configuration.Configuration('podcoder.ini')
    encoder.audio_encode(config, 'mp3')
    encoder.mp3_tag(config)
    encoder.mp3_coverart(config)
    encoder.audio_encode(config, 'ogg')
    encoder.ogg_tag(config)
    encoder.ogg_coverart(config)
    encoder.png_header(config)
    encoder.png_poster(config)
    encoder.mkv_encode(config)
    uploader.youtube_upload(config)

if __name__ == '__main__':
    main()
