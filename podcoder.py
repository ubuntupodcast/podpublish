#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

from podpublish import configuration
from podpublish import encoder

def main():
    config = configuration.Configuration('podcoder.ini')
    if not config.mp3['skip']:
        encoder.audio_encode(config, 'mp3')
        encoder.mp3_tag(config)
        encoder.mp3_coverart(config)

    if not config.ogg['skip']:
        encoder.audio_encode(config, 'ogg')
        encoder.ogg_tag(config)
        encoder.ogg_coverart(config)

    if not config.youtube['skip']:
        encoder.png_header(config)
        encoder.png_poster(config)
        encoder.mkv_encode(config)

if __name__ == '__main__':
    main()
