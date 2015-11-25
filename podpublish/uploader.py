#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import optparse
import os
import pysftp
import sys
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from youtube_upload import main as yt

def _sftp_put_file(config, cinfo, file_in):
    with pysftp.Connection(**cinfo) as sftp:
        print("Connected to: " + config.sftp['host'])
        print("Making directory: " + config.sftp['remote_directory'])
        sftp.makedirs(config.sftp['remote_directory'])
        with sftp.cd(config.sftp['remote_directory']):
            print("Changed to: " + config.sftp['remote_directory'])
            print("Putting: " + file_in)
            sftp.put(file_in)
            print("Setting permissions: 644")
            sftp.chmod(file_in, 644)

def sftp_upload(config, file_in):
    print("Uploading " + file_in + ' via sftp')

    if not config.sftp['remote_directory'].endswith('/'):
        config.sftp['remote_directory'] += '/'
        print('Added trailing / to:' + config.sftp['remote_directory'])

    if (config.sftp['username'] and config.sftp['password']) and not config.sftp['private_key']:
        print("Attempting to authenticate with username and password.")
        cinfo = {'host': config.sftp['host'],
                 'username': config.sftp['username'],
                 'password': config.sftp['password'],
                 'port': config.sftp['port']}

    elif (config.sftp['username'] and config.sftp['private_key']) and not config.sftp['private_key_pass']:
        print("Attempting to authenticate with username and private_key.")
        cinfo = {'host': config.sftp['host'],
                 'username': config.sftp['username'],
                 'private_key': config.sftp['private_key'],
                 'port': config.sftp['port']}

    elif config.sftp['username'] and config.sftp['private_key'] and config.sftp['private_key_pass']:
        print("Attempting to authenticate with username and private_key that has a passphrase.")
        cinfo = {'host': config.sftp['host'],
                 'username': config.sftp['username'],
                 'private_key': config.sftp['private_key'],
                 'private_key_pass': config.sftp['private_key_pass'],
                 'port': config.sftp['port']}

    _sftp_put_file(config, cinfo, file_in)

    # Check the file uploaded correctly.
    file_check = False
    with pysftp.Connection(**cinfo) as sftp:
        print("Connected to: " + config.sftp['host'])
        file_check = sftp.isfile(config.sftp['remote_directory'] + file_in)

    if not file_check:
        print('ERROR! Upload failed. Abort.')
        sys.exit(1)
    else:
        print('Upload completed.')

def wordpress_post(config):
    print("Connecting to: " + config.wordpress['xmlrpc'])
    wp = Client(config.wordpress['xmlrpc'],
                config.wordpress['username'],
                config.wordpress['password'])

    if config.attach_header:
        print("Uploading header image...")
        # Upload header image
        data = {
            'name': os.path.basename(config.png_header_file),
            'type': 'image/png',
        }

        # Read the image and let the XMLRPC library encode it to base64
        with open(config.png_header_file, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = wp.call(media.UploadFile(data))
        attachment_id = response['id']

    print("Posting blog...")
    post = WordPressPost()
    post.title = config.wordpress['title']
    post.content = config.wordpress['content']
    post.post_format = config.wordpress['post_format']
    post.post_status = config.wordpress['post_status']
    if config.attach_header:
        post.thumbnail = attachment_id
    post.terms_names = {
        'post_tag': [config.wordpress['tags']],
        'category': [config.wordpress['category']]
    }
    post.id = wp.call(NewPost(post))

def youtube_upload(config):
    print("Uploading " + config.mkv_file + ' to YouTube')

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
                 "--description=" + config.youtube['description'],
                 "--privacy=" + config.youtube['privacy'],
                 "--playlist=" + config.tags['album'],
                 "--client-secrets=" + config.youtube['client_secrets'],
                 "--credentials-file=" + config.youtube['credentials_file'],
                 "--tags=" + config.youtube['tags'],
                 "--publish-at=" + config.youtube['publish_at'],
                 config.mkv_file]

    options, args = parser.parse_args(arguments)
    #print(options)
    #print(args)
    yt.run_main(parser, options, args)

if __name__ == '__main__':
    pass
