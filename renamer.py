# !python 3

import os
import shutil
from pathlib import Path

import mutagen
from mutagen.id3 import ID3


# Program to rename all music files to the way i like it, with the track number - song title
# padded with an extra zero for tracks under 10
# To be called from the directory that is the root of all the music, D:\Music for me


# Used to clean up track numbers and print them the way that I like
# For example 02 - Start Me Up.mp3
def cleanUpTrackNumber(track):
    if ('/' in track):
        track = track[0:track.index('/')]
        if (int(track) < 10 and track[0] != '0'):
            track = '0' + track
    if (len(track) < 2):
        track = '0' + track
    if ('(' in track):
        track = track.replace('(', '')
        track = track.replace(')', '')
        track = track[0:track.index(',')]
        return cleanUpTrackNumber(track)
    return track

def handleMP3(musicFile, file):
    track = ''
    title = ''
    if ('TRCK' in musicFile.keys()):
        track = mutagen.id3.TRCK(musicFile.get('TRCK'))
        track = str(track[0])
        track = cleanUpTrackNumber(track)

    if ('TIT2' in musicFile.keys()):
        title = mutagen.id3.TIT2(musicFile.get('TIT2'))
        title = str(title[0])

    if (track and title):
        newTitle = track + " - " + title;
        indexOfLastDot = file.name.rfind('.')
        newTitle = newTitle + file.name[indexOfLastDot:]
        renameFile(file, newTitle)

def handleMP4(musicFile, file):
    track = ''
    title = ''
    if ('trkn' in musicFile.keys()):
        track = musicFile.get('trkn')[0]
        track = str(track)
        track = cleanUpTrackNumber(track)
    if ('©nam' in musicFile.keys()):
        title = musicFile.get('©nam')[0]

    if (track and title):
        newTitle = str(track) + " - " + str(title)
        indexOfLastDot = file.name.rfind('.')
        newTitle = newTitle + file.name[indexOfLastDot:]
        renameFile(file, newTitle)

def handleWMA(musicFile, file):
    if ('WM/TrackNumber' in musicFile.keys()):
        track = str(musicFile.get('WM/TrackNumber')[0])
        track = cleanUpTrackNumber(track)
    if ('Title' in musicFile.keys()):
        title = str(musicFile.get('Title')[0])

    if (track and title):
        newTitle = track + " - " + title
        indexOfLastDot = file.name.rfind('.')
        newTitle = newTitle + file.name[indexOfLastDot:]
        renameFile(file, newTitle)

def handleFLAC(musicFile, file):
    track = ''
    title = ''
    if ('tracknumber' in musicFile.keys()):
        track = str(musicFile.get('tracknumber')[0])
        track = cleanUpTrackNumber(track)
    if ('title' in musicFile.keys()):
        title = str(musicFile.get('title')[0])

    if (track and title):
        newTitle = track + " - " + title
        indexOfLastDot = file.name.rfind('.')
        newTitle = newTitle + file.name[indexOfLastDot:]
        renameFile(file, newTitle)

def renameFile(file, newTitle):
    if (file.name != newTitle):
        newTitle = newTitle.replace('?', '')
        newTitle = newTitle.replace(':', '')
        newTitle = newTitle.replace('*', '')
        newTitle = newTitle.replace('/', '')
        newTitle = newTitle.replace('\\', '_')
        newTitle = newTitle.replace('"', '')
        newTitle = newTitle.replace('_', '')
        newTitle = newTitle.replace('<', '')
        newTitle = newTitle.replace('>', '')
        newTitle.strip()
        newTitle.title()
        oldPath = str(Path(file).absolute())
        newPath = str(Path(file).absolute().parent) + "\\" + newTitle
        print("renaming " + file.name + " to " + newTitle)
        shutil.move(oldPath, newPath)

def doSomething(path):
    for x in path.iterdir():
        # if its directory, use recursion
        if (x.is_dir()):
            doSomething(x)
        if (x.is_file()):
            musicFile = mutagen.File(Path.absolute(x))
            if type(musicFile) == mutagen.mp3.MP3:
                handleMP3(musicFile, x)

            if type(musicFile) == mutagen.mp4.MP4:
                handleMP4(musicFile, x)

            if type(musicFile) == mutagen.asf.ASF:
                handleWMA(musicFile, x)

            if type(musicFile) == mutagen.flac.FLAC:
                handleFLAC(musicFile, x)

path = Path(os.getcwd())
print("Starting tree traversal in current path: " + os.getcwd())
doSomething(path)



