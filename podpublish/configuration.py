#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import configobj
import os
import random
import sys
import validate

def check_exists(file_in):
    if not os.path.isfile(file_in):
        print('ERROR! ' + file_in + ' was not found. Abort.')
        sys.exit(1)

class Configuration(object):

    def __init__(self, ini_file):
        # TODO: Use a ConfigSpec to validate the ini file.
        self.config = configobj.ConfigObj(ini_file)

        # expand any relative file paths.
        if self.config['artwork']['backdrop'].startswith('~'):
            self.config['artwork']['backdrop'] = os.path.expanduser(self.config['artwork']['backdrop'])

        if self.config['artwork']['coverart'].startswith('~'):
            self.config['artwork']['coverart'] = os.path.expanduser(self.config['artwork']['coverart'])

        if self.config['artwork']['font'].startswith('~'):
            self.config['artwork']['font'] = os.path.expanduser(self.config['artwork']['font'])

        if self.config['episode']['audio_in'].startswith('~'):
            self.config['episode']['audio_in'] = os.path.expanduser(self.config['episode']['audio_in'])

        if self.config['youtube']['client_secrets'].startswith('~'):
            self.config['youtube']['client_secrets'] = os.path.expanduser(self.config['youtube']['client_secrets'])

        if self.config['youtube']['credentials_file'].startswith('~'):
            self.config['youtube']['credentials_file'] = os.path.expanduser(self.config['youtube']['credentials_file'])

        if self.config['sftp']['private_key'].startswith('~'):
            self.config['sftp']['private_key'] = os.path.expanduser(self.config['sftp']['private_key'])

        # If backdrop is a directory, grab a random file from it.
        if os.path.isdir(self.config['artwork']['backdrop']):
            print("Backdrop is a directory, taking a lucky dip...")
            self.config['artwork']['backdrop'] = os.path.join(self.config['artwork']['backdrop'], random.choice(os.listdir(self.config['artwork']['backdrop'])))
            print("The winner is: " + self.config['artwork']['backdrop'])

        # Check that required files exist.
        check_exists(self.config['artwork']['backdrop'])
        check_exists(self.config['artwork']['coverart'])
        check_exists(self.config['artwork']['font'])

        #audio_in can be a directory for season_to_youtube
        if os.path.isdir(self.config['episode']['audio_in']):
            pass
        else:
            check_exists(self.config['episode']['audio_in'])
        check_exists(self.config['youtube']['client_secrets'])
        check_exists(self.config['youtube']['credentials_file'])
        if self.config['sftp']['private_key']:
            check_exists(self.config['sftp']['private_key'])

        # artwork
        self.backdrop = self.config['artwork']['backdrop']
        self.coverart = self.config['artwork']['coverart']
        if self.coverart.endswith('.png'):
            self.coverart_mime = 'image/png'
        elif self.coverart.endswith('.gif'):
            self.coverart_mime = 'image/gif'
        elif self.coverart.endswith('.jpg') or self.coverart.endswith('.jpeg'):
            self.coverart_mime = 'image/jpeg'

        self.font = self.config['artwork']['font']
        self.font_size = int(self.config['artwork']['font_size'])
        self.font_color = self.config['artwork']['font_color']
        self.line_color = self.config['artwork']['line_color']
        self.fill_color = self.config['artwork']['fill_color']
        self.fill_y_start = int(self.config['artwork']['fill_y_start'])
        self.fill_y_stop = int(self.config['artwork']['fill_y_stop'])
        self.img_header_width = int(self.config['artwork']['header_width'])
        self.img_header_height = int(self.config['artwork']['header_height'])
        self.img_poster_width = int(self.config['artwork']['poster_width'])
        self.img_poster_height = int(self.config['artwork']['poster_height'])

        # episode
        self.audio_in = self.config['episode']['audio_in']
        self.basename = self.config['episode']['basename']
        self.seperator = self.config['episode']['seperator']
        self.episode = self.config['episode']['number']
        self.episode_prefix = self.config['episode']['prefix']

        # mp3
        self.mp3 = self.config['mp3']

        # ogg
        self.ogg = self.config['ogg']

        # season
        self.season = self.config['season']['number']
        self.season_prefix = self.config['season']['prefix']

        # sftp
        self.sftp = self.config['sftp']
        self.sftp['port'] = int(self.sftp['port'])

        # tags
        self.tags = self.config['tags']

        # youtube
        self.youtube = self.config['youtube']

        # files
        self.episode_code = self.season_prefix + self.season + self.episode_prefix + self.episode
        self.file_out = self.basename + self.seperator + self.episode_code
        self.mkv_file = self.file_out + '.mkv'
        self.mp3_file = self.file_out + '.mp3'
        self.ogg_file = self.file_out + '.ogg'
        self.png_header_file = self.file_out + '_header.png'
        self.png_poster_file = self.file_out + '_poster.png'

        # what features are skipped
        self.skip_mp3 = self.config.get('mp3').as_bool('skip')
        self.skip_ogg = self.config.get('ogg').as_bool('skip')
        self.skip_sftp = self.config.get('sftp').as_bool('skip')
        self.skip_youtube = self.config.get('youtube').as_bool('skip')

    def update_filename(self):
        self.episode_code = self.season_prefix + self.season + self.episode_prefix + self.episode
        self.file_out = self.basename + self.seperator + self.episode_code
        self.mkv_file = self.file_out + '.mkv'
        self.mp3_file = self.file_out + '.mp3'
        self.ogg_file = self.file_out + '.ogg'
        self.png_header_file = self.file_out + '_header.png'
        self.png_poster_file = self.file_out + '_poster.png'

if __name__ == '__main__':
    pass
