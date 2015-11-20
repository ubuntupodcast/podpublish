#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import base64
import configobj
import sys
import validate
from ffmpy import FF
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.flac import Picture
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import APIC, COMM, ID3, error
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont

class Configuration(object):

    def __init__(self, ini_file):
        # FIXME: Add error checking
        self.config = configobj.ConfigObj(ini_file)

        # artwork
        self.coverart = self.config['artwork']['coverart']
        self.backdrop = self.config['artwork']['backdrop']
        self.font = self.config['artwork']['font']
        self.font_size = int(self.config['artwork']['font_size'])
        self.font_color = self.config['artwork']['font_color']
        self.line_color = self.config['artwork']['line_color']
        self.fill_color = self.config['artwork']['fill_color']
        self.fill_y_start = int(self.config['artwork']['fill_y_start'])
        self.fill_y_stop = int(self.config['artwork']['fill_y_stop'])
        self.img_header_width = int(self.config['artwork']['header_width'])
        self.img_header_height = int(self.config['artwork']['header_height'])

        # episode
        self.audio_in = self.config['episode']['audio_in']
        self.basename = self.config['episode']['basename']
        self.seperator = self.config['episode']['seperator']
        self.episode = self.config['episode']['number']
        self.episode_prefix = self.config['episode']['prefix']

        # mp3
        self.mp3_bitrate = self.config['mp3']['bitrate']
        self.mp3_channels = self.config['mp3']['channels']

        # ogg
        self.ogg_bitrate = self.config['ogg']['bitrate']
        self.ogg_channels = self.config['ogg']['channels']

        # season
        self.season = self.config['season']['number']
        self.season_prefix = self.config['season']['prefix']

        # tags
        self.tags = self.config['tags']

        # files
        self.file_out = self.basename + self.seperator + self.season_prefix + self.season + self.episode_prefix + self.episode
        self.mkv_file = self.file_out + '.mkv'
        self.mp3_file = self.file_out + '.mp3'
        self.ogg_file = self.file_out + '.ogg'
        self.png_header_file = self.file_out + '_header.png'
        self.png_poster_file = self.file_out + '_poster.png'

def mp3_encode(config):
    print("Encoding " + config.mp3_file)
    AudioSegment.from_file(config.audio_in).export(config.mp3_file,
        bitrate=config.mp3_bitrate,
        format='mp3',
        parameters=['-ac', config.mp3_channels]
        )

def mp3_tag(config):
    print("Tagging " + config.mp3_file)
    # Make sure the MP3 has tag headers.
    try:
        audio = EasyID3(config.mp3_file)
    except mutagen.id3.error:
        audio = EasyID3()
        audio.save(config.mp3_file)

    # Add the tags.
    for k in config.tags.keys():
        if k == 'comments':
            continue
        else:
            try:
                audio[k] = config.tags[k]
            except EasyID3KeyError:
                print("%s is an invalid ID3 key" % k)
    audio.save(config.mp3_file)

    # Comments are not supported via EasyID3
    audio = ID3(config.mp3_file)
    audio["COMM"] = COMM(encoding=3, lang=config.tags['language'], desc='desc', text=config.tags['comments'])
    audio.save(config.mp3_file)

def mp3_coverart(config):
    print("Adding cover art to " + config.mp3_file)
    imgdata = open(config.coverart,'rb').read()

    audio=MP3(config.mp3_file, ID3=ID3);
    # FIXME: Derive the image mime type.
    audio.tags.add(APIC(encoding=3,
                        mime='image/png',
                        type=3,
                        desc=u'Cover',
                        data=imgdata))
    audio.save()


def ogg_encode(config):
    print("Encoding " + config.ogg_file)
    AudioSegment.from_file(config.audio_in).export(config.ogg_file,
        bitrate=config.ogg_bitrate,
        format='ogg',
        codec='libvorbis',
        parameters=['-ac', config.ogg_channels]
        )

def ogg_tag(config):
    print("Tagging " + config.ogg_file)
    audio = OggVorbis(config.ogg_file)

    # Add the tags.
    for k in config.tags.keys():
        audio[k] = config.tags[k]
    audio.save()

def ogg_coverart(config):
    print("Adding cover art to " + config.ogg_file)
    coverart = config.coverart
    imgdata = open(coverart,'rb').read()

    im = Image.open(coverart)
    w,h = im.size

    p = Picture()
    p.data = imgdata
    p.type = 3
    p.desc = u'Cover'
    # FIXME: Derive the image mime type.
    p.mime = 'image/png';
    p.width = w
    p.height = h
    p.depth = 24
    dt=p.write();
    enc=base64.b64encode(dt).decode('ascii');

    audio = OggVorbis(config.ogg_file)
    audio['metadata_block_picture']=[enc];
    audio.save()

def img_resize(img_file, width, height):
    #response = requests.get(headerimageurl)
    img = Image.open(img_file)

    # Check the image size.
    if img.size[0] < width or img.size[1] < height:
        print("Sorry, the image needs to larger than the requested resize. Abort.")
        sys.exit(1)

    scale_x_down_by = img.size[0] // width
    scale_y_down_by = img.size[1] // height

    if scale_x_down_by > scale_y_down_by:
        resize_to = (int(img.size[0] // scale_y_down_by), height)
        x_border = int(resize_to[0]) - width
        crop = (x_border // 2, 0, width + (x_border // 2), height)
    else:
        resize_to = (width, int(img.size[1] // scale_x_down_by))
        y_border = int(resize_to[1]) - height
        crop = (0, y_border // 2, width, height + (y_border // 2))
    img.thumbnail(resize_to, Image.ANTIALIAS)
    cropped = img.crop(crop)
    return cropped

def png_header(config):
    print("Creating " + config.png_header_file)
    header = img_resize(config.backdrop, config.img_header_width, config.img_header_height)
    header.save(config.png_header_file)

def png_poster(config):
    # Poster images for use in YouTube videos are hardcoded to 854x480.
    # No pressing need for higher resolution images for still videos.
    print("Creating " + config.png_poster_file)
    artist = config.tags['artist']
    title = config.tags['album'] + ' ' + config.tags['title']
    font = ImageFont.truetype(config.font, config.font_size)

    image = img_resize(config.backdrop, config.img_header_width, config.img_header_height)
    image.thumbnail((854, 534), Image.ANTIALIAS)
    poster = image.crop((0,(534-480)//2,854,534-((534-480)//2)))

    draw = ImageDraw.Draw(poster)
    draw.rectangle(((0,config.fill_y_start),(854,config.fill_y_stop)), fill=config.fill_color)

    artist_w,artist_h = font.getsize(artist)
    artist_x_offset = (854 - artist_w) // 2

    # Write artist and underline it
    draw.text((artist_x_offset, config.fill_y_start), artist, fill=config.font_color, font=font)
    draw.line(((artist_x_offset, config.fill_y_start + artist_h + 4),(854 - artist_x_offset, config.fill_y_start + artist_h + 4)), fill=config.line_color)

    fontsize = config.font_size
    while True:
        font = ImageFont.truetype(config.font, fontsize)
        title_w, title_h = font.getsize(title)
        if title_w < 854 - fontsize:
            break
        fontsize -= 1
        print('Resizing font so the title fits: ' + str(fontsize))
        if fontsize == 1:
            font = ImageFont.truetype(config.font, config.font_size // 2)

    title_y_offset = config.fill_y_start + artist_h + 8
    draw.text(((854 - title_w) // 2, title_y_offset), title, fill=config.font_color, font=font)
    del draw

    poster.save(config.png_poster_file)

def mkv_encode(config):
    ff = FF(global_options='-hide_banner -y -loop 1 -framerate 1',
            inputs={config.png_poster_file: None, config.audio_in: None},
            outputs={config.mkv_file: '-c:v libx264 -preset fast -tune stillimage -crf 18 -c:a aac -strict experimental -b:a 160k -shortest -pix_fmt yuv420p'})
    print(ff.cmd_str)
    ff.run()

if __name__ == '__main__':
    config = Configuration('podcoder.ini')
    mp3_encode(config)
    mp3_tag(config)
    mp3_coverart(config)
    ogg_encode(config)
    ogg_tag(config)
    ogg_coverart(config)
    png_header(config)
    png_poster(config)
    mkv_encode(config)
