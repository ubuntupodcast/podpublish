#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import optparse
from youtube_upload import main as yt

def youtube_upload(config):
    print("Uploading " + config.mkv_file + ' to YouTube')
    # The reference YouTube API provided by doesn't support playlists,
    # so wrap youtube-upload instead.
    #  * https://github.com/tokland/youtube-upload
    #  * https://www.youtube.com/watch?v=IX8xlnk54Mg

    parser = optparse.OptionParser()
    # Video metadata
    parser.add_option('', '--title', dest='title', type="string")
    parser.add_option('', '--category', dest='category', type="string")
    parser.add_option('', '--description', dest='description', type="string")
    parser.add_option('', '--tags', dest='tags', type="string")
    parser.add_option('', '--privacy', dest='privacy', metavar="STRING", default="public")
    parser.add_option('', '--publish-at', dest='publish_at', metavar="datetime", default=None)
    parser.add_option('', '--location', dest='location', type="string", default=None, metavar="latitude=VAL,longitude=VAL[,altitude=VAL]")
    parser.add_option('', '--thumbnail', dest='thumb', type="string")
    parser.add_option('', '--playlist', dest='playlist', type="string")
    parser.add_option('', '--title-template', dest='title_template', type="string", default="{title} [{n}/{total}]", metavar="STRING")
    # Authentication
    parser.add_option('', '--client-secrets', dest='client_secrets', type="string")
    parser.add_option('', '--credentials-file', dest='credentials_file', type="string")
    parser.add_option('', '--auth-browser', dest='auth_browser', action='store_true')
    #Additional options
    parser.add_option('', '--open-link', dest='open_link', action='store_true')

    arguments = ["--title=" + config.tags['album'] + " " + config.tags['title'],
                 "--category=" + config.youtube['category'],
                 "--description=" + config.tags['comments'],
                 "--privacy=" + config.youtube['privacy'],
                 "--playlist=" + config.tags['album'],
                 "--client-secrets=" + config.youtube['client_secrets'],
                 "--credentials-file=" + config.youtube['credentials_file'],
                 "--tags=" + config.youtube['tags'],
                 config.mkv_file]

    options, args = parser.parse_args(arguments)
    yt.run_main(parser, options, args)

if __name__ == '__main__':
    pass
