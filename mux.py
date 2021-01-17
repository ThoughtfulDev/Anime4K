import glob, os, sys, subprocess
from pymkv import MKVFile, MKVTrack
from utils import langToShort, shortToLong



def addAudio(source, ext):
    for file in glob.glob("*." + ext):
        t = MKVTrack(file)
        lang = file.split('.')[0]
        t.track_name = lang
        t.language = langToShort(lang)
        print("Adding AudioTrack")
        source.add_track(t)

def addSubs(source, ext):
    for file in glob.glob("*." + ext):
        t = MKVTrack(file)
        lang = file.split('.')[0]
        if "_" in lang:
            lang = lang.split('_')[0]
        else:
            lang = lang
        t.track_name = shortToLong(lang)
        t.language = lang
        print("Adding new SUB")
        source.add_track(t)

def delete_by_extension(ext):
    for file in glob.glob("*." + ext):
        os.remove(file)
        
def mux(fn, out):
    mkv = MKVFile(fn)

    addAudio(mkv, "AAC")
    addAudio(mkv, "MP3")
    addAudio(mkv, "DTS")
    addAudio(mkv, "Opus")
    addAudio(mkv, "FLAC")
    addAudio(mkv, "TrueHD Atmos")
    addAudio(mkv, "AC-3")
    addAudio(mkv, "DTS-HD Master Audio")

    addSubs(mkv, "sup")
    addSubs(mkv, "srt")
    addSubs(mkv, "ass")

    mkv.mux(out)

    #clean up
    print("Cleaning...")

    delete_by_extension("AAC")
    delete_by_extension("MP3")
    delete_by_extension("DTS")
    delete_by_extension("Opus")
    delete_by_extension("FLAC")
    delete_by_extension("TrueHD Atmos")
    delete_by_extension("AC-3")
    delete_by_extension("DTS-HD Master Audio")

    delete_by_extension("sup")
    delete_by_extension("srt")
    delete_by_extension("ass")
    print("KTHXBYE")