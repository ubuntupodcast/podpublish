#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import glob
import os
import re
import sys
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.oggvorbis import OggVorbis
from podpublish import podcoder

def get_files(audio_in, audio_format):
    files = [os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(audio_in)
        for f in files if f.endswith(audio_format)]
    return files

def get_tags(audio_file, audio_format):
    print("Getting tags from " + audio_file)
    if audio_format is 'mp3':
        return EasyID3(audio_file)
    elif audio_format is 'ogg':
        return OggVorbis(audio_file)
    else:
        print("ERROR! Unknown audio format. Abort.")
        sys.exit(1)

def main():
    AUDIO_FORMAT='ogg'

    config = podcoder.Configuration('/home/martin/Dropbox/UbuntuPodcast/YouTube/s01.ini')
    audio_files = get_files(config.audio_in, AUDIO_FORMAT)

    for audio_file in audio_files:
        # Ignore the low bitrate files
        if '_low' in audio_file:
            continue

        # Pull in the episode from the mp3 filename.
        config.episode = re.findall(r"(?:e|x|episode|\n)(\d{2})", audio_file, re.I)[0]
        config.update_filename()

        if not os.path.isfile(config.mkv_file):
            # Update the configuration to point at the current audio file.
            config.audio_in = audio_file
            tags = get_tags(audio_file, AUDIO_FORMAT)

            # Pull in the title from the mp3 tags.
            config.tags['title'] = tags['title'][0]

            podcoder.png_poster(config)
            podcoder.mkv_encode(config, True)
            os.remove(config.png_poster_file)

        # TODO: Check if the file is already uploaded.
        #youtube_upload(config)

if __name__ == '__main__':
    main()
