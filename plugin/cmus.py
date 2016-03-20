#!/usr/bin/python
import sys
import commands
import subprocess
import re

# check if pyfribidi is installed
try:
    import pyfribidi
    hasFribidi = True
except ImportError:
    hasFribidi = False
    pass

CMUS_REMOTE = 'cmus-remote'

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

def toInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

def visualizeIfUnicode(s):
    return pyfribidi.log2vis(s, base_direction=pyfribidi.ON
            ).decode('utf-8')

def parseCmusStdout(arguments):
    errors = ''
    proc   = subprocess.Popen(arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    for line in iter(proc.stdout.readline, b''):
        match = re.match(r'^(.*)(cmus-remote: )(.*)$', line, re.M|re.I)
        if match:
            errors = match.group(3)
            break
        match = re.match(r'^status\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['status'] = match.group(1)
            continue
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
    return errors


def makeResultStatus(errors):
    if errors:
        print(errors)
    else:
        print('new options has been sent')

def makeTaggedStatus():
    if hasFribidi:
        tags['artist'] = visualizeIfUnicode(tags['artist'])
        tags['album']  = visualizeIfUnicode(tags['album'])
        tags['title']  = visualizeIfUnicode(tags['title'])

    statusMessage = u'\u266a {t[status]}: {t[artist]} '.format(t=tags)
    if tags['album']:
        statusMessage += u' \u266c  {t[album]}{t[date]} '.format(t=tags)

    statusMessage += u' \u266b  {t[track]}{t[title]}'.format(t=tags)

    print(statusMessage.encode('utf-8'))


#------------------------------------------------------------------------------
# check if cmus is already installed
cmus_path  = commands.getoutput('which {}'.format(CMUS_REMOTE))
if cmus_path is None or len(cmus_path) == 0:
    print 'cmus is not installed. https://cmus.github.io/'
else:
    tags       = {'status':'', 'artist':'', 'album':'', 'title':'', 'track':'', 'date':''}
    userAction = sys.argv[1]
    isVimMode  = sys.argv[0] == 'vim_mode'
    cmusArgs   = CMUS_DICTIONARY.get(userAction, None)
    if cmusArgs is not None and len(cmusArgs) > 0:
        errors = parseCmusStdout([cmus_path] + cmusArgs)
        if not tags['status']:
            makeResultStatus(errors)
        else:
            makeTaggedStatus()

