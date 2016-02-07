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
def cmusAction(verb):
    if verb:
        if   verb == 'prev'   : return ['--prev',  '-Q']
        elif verb == 'next'   : return ['--next',  '-Q']
        elif verb == 'pause'  : return ['--pause', '-Q']
        elif verb == 'play'   : return ['--play',  '-Q']
        elif verb == 'stop'   : return ['--stop',  '-Q']
        elif verb == 'curr'   : return ['-Q']
        elif verb == 'all'    : return ['--raw', r'set aaa_mode=all']
        elif verb == 'artist' : return ['--raw', r'set aaa_mode=artist']
        elif verb == 'album'  : return ['--raw', r'set aaa_mode=album']

    return None

def doneFor(verb):
    if verb:
        if verb == 'prev' or verb == 'next' or verb == 'play' or verb == 'curr':
            return 'playing'
        elif verb == 'pause':
            return 'paused'
        elif verb == 'stop':
            return 'stopped'
        elif verb == 'all' or verb == 'artist' or verb == 'album':
            print('new options has been set')
            return None

    return 'info'

def toInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

def visualizeIfUnicode(s):
    return pyfribidi.log2vis(s, base_direction=pyfribidi.ON)

# runs a command and returns an line iterator for stdout
def runCommand(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    return iter(p.stdout.readline, b'')

def parseCmusStdout(arguments):
    tags    = {'artist':'', 'album':'', 'title':'', 'track':'', 'date':''}
    command = ['/usr/local/bin/cmus-remote'] + arguments
    proc    = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
        match = re.match(r'^tag artist\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['artist'] = match.group(1)

        match = re.match(r'^tag album\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['album'] = match.group(1)

        match = re.match(r'^tag title\s+(.*)\s+$', line, re.M|re.I)
        if match:
            tags['title'] = match.group(1)

        match = re.match(r'^tag date\s+(.*)\s+$', line, re.M|re.I)
        if match:
            dateNo = toInt(match.group(1))
            if dateNo > 0:
                tags['date']  = ' (@{})'.format(dateNo)

        match = re.match(r'^tag tracknumber\s+(.*)\s+$', line, re.M|re.I)
        if match:
            trackId = toInt(match.group(1))
            if trackId > 0:
                tags['track'] = '{}) '.format(trackId)

    done = doneFor(userAction)
    if done is not None:
        if hasFribidi:
            tags['artist'] = visualizeIfUnicode(tags['artist']).decode('utf-8')
            tags['album']  = visualizeIfUnicode(tags['album']).decode('utf-8')
            tags['title']  = visualizeIfUnicode(tags['title']).decode('utf-8')

        statusMessage = u'\u266a {}: {t[artist]} '.format(
                doneFor(userAction), t=tags
                )
        if tags['album']:
            statusMessage += u' \u266c  {t[album]}{t[date]} '.format(t=tags)

        statusMessage += u' \u266b  {t[track]}{t[title]}'.format(t=tags)

        print(statusMessage)


userAction = sys.argv[1]
args       = cmusAction(userAction)
if args is not None and len(args) > 0:
    parseCmusStdout(args)

