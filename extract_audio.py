from pymkv import MKVFile
from simple_term_menu import TerminalMenu
import subprocess, sys, os, glob, time
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
    
    flacs = []
    for file in glob.glob("*.FLAC"):
            flacs.append(file)
    if len(flacs) > 0:
        convert_menu = TerminalMenu(["Yes", "No"], title="Do you want to convert every FLAC to Opus?")
        convert_choice = convert_menu.show()
        if convert_choice == 0:
            for f in flacs:
                br_menu = TerminalMenu(["Stereo", "5.1", "7.1"], title="Whats the format of the file? => {0}".format(f))
                br_choice = br_menu.show()
                if br_choice == 0:
                    br = "192K"
                elif br_choice == 1:
                    br = "384K"
                elif br_choice == 2:
                    br = "512K"
                else:
                    br = "192K"
                fn_base = f.split(".")[0]
                out_audio = fn_base + ".Opus"
                subprocess.call([
                    "ffmpeg",
                    "-hide_banner",
                    "-i",
                    f,
                    "-c:a",
                    "libopus",
                    "-b:a",
                    br,
                    "-vbr",
                    "on",
                    out_audio
                ])
                time.sleep(1)
                os.remove(f)