#!/usr/bin/python
import sys
import subprocess
import re

# check if pyfribidi is installed
try:
    import pyfribidi
    hasFribidi = True
except ImportError:
    hasFribidi = False
    pass

# make an equivalent for cmus-remote call
CMUS_DICTIONARY = {
        'curr':   ['-Q'],
        'prev':   ['--prev',  '-Q'],
        'next':   ['--next',  '-Q'],
        'pause':  ['--pause', '-Q'],
        'play':   ['--play',  '-Q'],
        'stop':   ['--stop',  '-Q'],
        'all':    ['--raw',   r'set aaa_mode=all'],
        'artist': ['--raw',   r'set aaa_mode=artist'],
        'album':  ['--raw',   r'set aaa_mode=album']
        }

def whatHasBeenDone(verb):
    if verb:
        if verb == 'curr' or verb == 'play':
            return 'playing'
        elif verb == 'prev' or verb == 'next':
            return 'play'
        elif verb == 'pause':
            return 'paused'
        elif verb == 'stop':
            return 'stopped'
        elif verb == 'all' or verb == 'artist' or verb == 'album':
            print('new options has been sent')
            return None

    return 'info'

def toInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

def visualizeIfUnicode(s):
    return pyfribidi.log2vis(s, base_direction=pyfribidi.ON
            ).decode('utf-8')

def parseCmusStdout(arguments):
    proc    = subprocess.Popen(arguments, stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
        match = re.match(r'^tag artist\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['artist'] = match.group(1)
            continue

        match = re.match(r'^tag album\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['album'] = match.group(1)
            continue

        match = re.match(r'^tag title\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['title'] = match.group(1)
            continue

        match = re.match(r'^tag date\s+(.*)\s+$', line, re.M|re.I)
        if match:
            dateNo = toInt(match.group(1))
            if dateNo > 0: #append date only if reported > 0
                tags['date']  = ' (@{})'.format(dateNo)
            continue

        match = re.match(r'^tag tracknumber\s+(.*)\s+$', line, re.M|re.I)
        if match:
            trackId = toInt(match.group(1))
            if trackId > 0: #prepend track number only if > 0
                tags['track'] = '{}) '.format(trackId)
            continue


def makeStatusMessage(done):
    if done is None:
        return

    if hasFribidi:
        tags['artist'] = visualizeIfUnicode(tags['artist'])
        tags['album']  = visualizeIfUnicode(tags['album'])
        tags['title']  = visualizeIfUnicode(tags['title'])

    statusMessage = u'\u266a {}: {t[artist]} '.format(done, t=tags)
    if tags['album']:
        statusMessage += u' \u266c  {t[album]}{t[date]} '.format(t=tags)

    statusMessage += u' \u266b  {t[track]}{t[title]}'.format(t=tags)

    print(statusMessage)


#------------------------------------------------------------------------------

tags       = {'artist':'', 'album':'', 'title':'', 'track':'', 'date':''}
userAction = sys.argv[1]
isVimMode  = sys.argv[0] == 'vim_mode'
cmusArgs   = CMUS_DICTIONARY.get(userAction, None)
if cmusArgs is not None and len(cmusArgs) > 0:
    parseCmusStdout(['cmus-remote'] + cmusArgs)
    makeStatusMessage(whatHasBeenDone(userAction))

