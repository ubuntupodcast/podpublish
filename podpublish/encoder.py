#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import base64
import ffmpy
import sys
from collections import OrderedDict
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.flac import Picture
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import APIC, COMM, ID3, error
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage

def audio_encode(config, audio_format):
    if audio_format is 'mp3':
        audio_file = config.mp3_file
        audio_bitrate = config.mp3['bitrate']
        audio_channels = config.mp3['channels']
        audio_codec = 'libmp3lame'
    elif audio_format is 'ogg':
        audio_file = config.ogg_file
        audio_bitrate = config.ogg['bitrate']
        audio_channels = config.ogg['channels']
        audio_codec = 'libvorbis'
    else:
        print("ERROR! Unkown audio format requested. Abort.")
        sys.exit(1)

    print("Encoding " + audio_file)
    AudioSegment.from_file(config.audio_in).export(audio_file,
        bitrate=audio_bitrate,
        codec=audio_codec,
        format=audio_format,
        parameters=['-ac', audio_channels]
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
    print("Adding " + config.coverart_mime +  " cover art to " + config.mp3_file)
    imgdata = open(config.coverart,'rb').read()

    audio=MP3(config.mp3_file, ID3=ID3);
    audio.tags.add(APIC(encoding=3,
                        mime=config.coverart_mime,
                        type=3,
                        desc='Cover',
                        data=imgdata))
    audio.save()

def ogg_tag(config):
    print("Tagging " + config.ogg_file)
    audio = OggVorbis(config.ogg_file)

    # Add the tags.
    for k in config.tags.keys():
        audio[k] = config.tags[k]
    audio.save()

def ogg_coverart(config):
    print("Adding " + config.coverart_mime +  " cover art to " + config.ogg_file)
    coverart = config.coverart
    imgdata = open(coverart,'rb').read()

    im = Image.open(coverart)
    w,h = im.size

    p = Picture()
    p.data = imgdata
    p.type = 3
    p.desc = 'Cover'
    p.mime = config.coverart_mime
    p.width = w
    p.height = h
    p.depth = 24
    dt=p.write()
    enc=base64.b64encode(dt).decode('ascii')

    audio = OggVorbis(config.ogg_file)
    audio['metadata_block_picture']=[enc]
    audio.save()

def png_header(config):
    print("Creating " + config.png_header_file)
    with open(config.backdrop, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [config.img_header_width, config.img_header_height])
            cover.save(config.png_header_file, 'png')

def png_poster(config):
    print("Creating " + config.png_poster_file)
    artist = config.tags['artist']
    title = config.tags['album'] + ' ' + config.tags['title']
    font = ImageFont.truetype(config.font, config.font_size)

    with open(config.backdrop, 'r+b') as f:
        with Image.open(f) as image:
            poster = resizeimage.resize_cover(image, [config.img_poster_width, config.img_poster_height])

    draw = ImageDraw.Draw(poster)
    draw.rectangle(((0,config.fill_y_start),(config.img_poster_width, config.fill_y_stop)), fill=config.fill_color)

    artist_w,artist_h = font.getsize(artist)
    artist_x_offset = (config.img_poster_width - artist_w) // 2

    # Write artist and underline it
    draw.text((artist_x_offset, config.fill_y_start), artist, fill=config.font_color, font=font)
    draw.line(((artist_x_offset, config.fill_y_start + artist_h + 4),(config.img_poster_width - artist_x_offset, config.fill_y_start + artist_h + 4)), fill=config.line_color)
    draw.line(((artist_x_offset, config.fill_y_start + artist_h + 5),(config.img_poster_width - artist_x_offset, config.fill_y_start + artist_h + 5)), fill=config.line_color)

    fontsize = config.font_size
    while True:
        font = ImageFont.truetype(config.font, fontsize)
        title_w, title_h = font.getsize(title)
        if title_w < config.img_poster_width - fontsize:
            break
        fontsize -= 1
        if fontsize == 1:
            print("ERROR! Can't fit title on the poster. Abort.")
            sys.exit(1)

    title_y_offset = config.fill_y_start + artist_h + 8
    draw.text(((config.img_poster_width - title_w) // 2, title_y_offset), title, fill=config.font_color, font=font)
    del draw

    poster.save(config.png_poster_file, 'png')

def mkv_encode(config, copy_audio = False):
    # Reference for encoding
    #  - https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/

    # If animated_video is True then overlay an animated waveform, otherwise
    # just use the static poster image and audio.

    # Only x264 has the `-tune` option so set to empty by default.
    if config.animated_video:
        print("Encoding animated " + config.mkv_file)
        frate=24
        loop=0
        if config.fill_y_stop >= config.img_poster_height:
            filter_y = config.fill_y_start - (config.fill_y_stop - config.fill_y_start)
        else:
            filter_y = config.fill_y_stop

        filter_complex='-filter_complex "[0:v]null[bg];[1:a]showwaves=s=' + str(config.img_poster_width) + 'x' + str(config.img_poster_height // 3) +':mode=line:rate=' + str(frate // 2) + ':colors=' + config.line_color + ':scale=lin[fg];[bg][fg]overlay=0:' + str(filter_y) + ',colorkey=' + config.fill_color + '" '
        tune_stillimage=' '
    else:
        print("Encoding static " + config.mkv_file)
        frate = 1
        loop = 1
        filter_complex = ''
        tune_stillimage = ' -tune stillimage '

    audio_filter = ' -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" '
    if copy_audio:
        audio_params = '-c:a copy'
    else:
        audio_params = '-c:a aac -r:a 44100 -strict experimental -b:a 384k'

    # Tweak the encoder options.
    if config.codec == 'h264_vaapi':
        vaapi_device = ' -vaapi_device /dev/dri/renderD128 '
        video_filter = " -vf 'format=nv12,hwupload' "
        preset=' -quality 8 '
        tune_stillimage=' '
    elif config.codec == 'h264_nvenc':
        vaapi_device = ''
        video_filter = ''
        preset=' -preset fast '
        tune_stillimage=' '
    else:
        vaapi_device = ''
        video_filter = ''
        preset=' -preset ultrafast '

    global_options='-hide_banner -y -loop ' + str(loop) + ' -framerate ' + str(frate)
    inputs = OrderedDict([(config.png_poster_file, '-pix_fmt rgb24'), (config.audio_in, None)])
    outputs = OrderedDict([(config.mkv_file, vaapi_device + filter_complex + video_filter + '-c:v ' + config.codec + ' -pix_fmt yuv420p ' + preset + '-bf 2 -flags +cgop' + tune_stillimage + audio_filter + audio_params + ' -shortest -movflags faststart')])
    ff = ffmpy.FFmpeg(global_options=global_options, inputs=inputs, outputs=outputs)
    print(ff.cmd)
    ff.run()

if __name__ == '__main__':
    pass
