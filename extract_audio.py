from pymkv import MKVFile
import subprocess, sys, os
from utils import language_mapping, is_tool

def extract_audio(fn):
    mkv = MKVFile(fn)

    tracks = mkv.get_track()
    for track in tracks:
        if track.track_type == 'audio':
            ext = track._track_codec
            lang = language_mapping[track._language]
            id = str(track._track_id)
            subprocess.call(['mkvextract', 'tracks', fn, id + ':' + lang + '.' + ext])