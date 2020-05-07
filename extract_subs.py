from pymkv import MKVFile
import subprocess, sys, os
from utils import is_tool


def genExt(codec):
    if "PGS" in codec:
        return "sup"
    elif "ASS" in codec or "SubStationAlpha" in codec:
        return "ass"
    elif "SRT" in codec or "SubRip" in codec:
        return "srt"

def extract_subs(fn):
    mkv = MKVFile(fn)

    tracks = mkv.get_track()
    for track in tracks:
        if track.track_type == 'subtitles':
            ext = genExt(track._track_codec)
            lang = track._language
            id = str(track._track_id)
            
            subprocess.call(['mkvextract', 'tracks', fn, id + ':' + lang + '_' + id + '.' + ext])
        
        