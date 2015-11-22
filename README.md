# Introduction

A tool for encoding and publishing podcast content and assets. Inspired
by:

  * https://github.com/stuartlangridge/bv-publish

Project created by [Ubuntu Podcast](http://www.ubuntupodcast.org) and
released under the [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
license.

## Installation

Eventually this will be added to PyPi (or something) for simplier
installation. But for now the following steps are required, which
assume you're running Ubuntu.

### Install ffmpeg and pip

    sudo apt-get install ffmpeg libavcodec-extra python3-pip

### Install podpublish

    git clone git@bitbucket.org:flexiondotorg/podpublish.git
    sudo pip3 install -r podpublish/requirements.txt

## Usage

This project is a work in progress and still somewhat hardcoded but
will soon be made into a generic tool useful to other podcasters.

### Encoding a single podcast

To encode an audio file to `.mp3`, `.ogg` and `.mkv` (for uploading to
YouTube, do the following.

  * Edit the example `podcoder.ini`.
  * Execute `./podcoder.py`.

### Encoding a season of podcasts

To encode a season of audio files, either in `.mp3` or `.ogg` format,
to `.mkv` and uploading them to YouTube, do the following.

  * Edit the example `season-to-youtube.ini`.
  * Execute `./season-to-youtube.py`.

The season encoder/uploader expects derive the each Episode number from
the source audio filename and each episode Title from tags embedded in
the source audio files.

### YouTube API

To upload to YouTube you'll need a Google account with associated
YouTube channel, the YouTube Data API will need to be enabled and
OAuth 2.0 client-secret generated.

The reference YouTube API provided by doesn't support playlists, or
setting a publishing date, so [youtube-upload](https://github.com/tokland/youtube-upload)
is used instead. The following video maybe helpful in enabling the
YouTube Data API and creating client secrets.

  * https://www.youtube.com/watch?v=IX8xlnk54Mg

### Uploading via sftp

This is how to create an account, on Ubuntu, that has sftp access via
key based authentication.

#### On your workstation

Generate a ssh key pair. This will create `~/PodPublish.key`
(the private key) and `~/PodPublish.pub` (the public key).

    ssh-keygen -b 4096 -t rsa -N yoursupersecretpassphrase -C "Podcast Publisher" -f ~/PodPublish

#### On the server

    sudo apt-get install ssh
    sudo adduser --gecos "Podcast Publisher" --disabled-password yourusername

As `root` do the following on the server to create the `authorized_keys`
file.

    mkdir /home/yourusername/.ssh

Add the content of  `~/PodPublish.pub` to /home/yourusername/.ssh/

    nano /home/yourusername/.ssh/authorized_keys

    chmod 600 /home/yourusername/.ssh/authorized_keys
    chmod 700 /home/yourusername/.ssh/
    chown -R yourusername: /home/yourusername/.ssh

## Source Code

Source code is available from BitBucket.

  * https://bitbucket.org/flexiodotorg/podpublish
