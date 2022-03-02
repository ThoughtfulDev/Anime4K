import subprocess, os, glob
from simple_term_menu import TerminalMenu
from utils import is_tool, clear



def encode_to_hevc(fn, out, opts=None):
    param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.0"
    
    if opts == None:
        detail_menu = TerminalMenu([
            "(Recommended if you dont know) One Setting to rule them all",
            "(e.g Your Name) Flat, slow anime (slice of life, everything is well lit)",
            "(e.g Kimetsu no Yaiba) Some dark scene, some battle scene (shonen, historical, etc.)",
            "(Rarely used) [TV Series] Movie-tier dark scene, complex grain/detail",
            "(Rarely used) [Movie] Movie-tier dark scene, complex grain/detail",
        ], title="Choose the encode options")

        choice = detail_menu.show()
    else:
        choice = int(opts['encode']['mode'])
    # Flat, slow anime (slice of life, everything is well lit)
    if choice == 1:
        param_line = "crf=19.0:bframes=8:aq-mode=3:psy-rd=1:aq-strength=0.8:deblock=1,1"
    #Some dark scene, some battle scene (shonen, historical, etc.)
    elif choice == 2:
        param_line = "crf=18.0:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=2"
    #[TV Series] Movie-tier dark scene, complex grain/detail
    elif choice == 3:
        param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"
    #[Movie] Movie-tier dark scene, complex grain/detail
    elif choice == 4:
        param_line = "crf=16.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"
    
    
    
    if is_tool("ffmpeg-bar"):
        binary = "ffmpeg-bar"
    else:
        binary = "ffmpeg"

    files = []
    if os.path.isdir(fn):   
        for file in glob.glob(os.path.join(fn, "*.mkv")):
            files.append(os.path.join(file))
    if len(files) == 0:
        cmd = [
        binary,
        "-hide_banner",
        "-i",
        fn,
        "-c:v",
        "libx265",
        "-profile:v",
        "main10",
        "-pix_fmt",
        "yuv420p10le",
        "-preset",
        "slow",
        "-x265-params",
        param_line,
        "-map",
        "0:v:0",
        "-f",
        "matroska",
        '-vf',
        'scale=out_color_matrix=bt709',
        '-color_primaries',
        'bt709',
        '-color_trc',
        'bt709',
        '-colorspace',
        'bt709',
        out
        ]  
        subprocess.call(cmd)
    else:
        for f in files:
            clear()
            name = f.split("/")
            name = name[len(name) - 1]
            cmd = [
            binary,
            "-hide_banner",
            "-i",
            f,
            "-c:v",
            "libx265",
            "-profile:v",
            "main10",
            "-pix_fmt",
            "yuv420p10le",
            "-preset",
            "slow",
            "-x265-params",
            param_line,
            "-map",
            "0:v:0",
            "-f",
            "matroska",
            '-vf',
            'scale=out_color_matrix=bt709',
            '-color_primaries',
            'bt709',
            '-color_trc',
            'bt709',
            '-colorspace',
            'bt709',
            os.path.join(out, name)
            ]  
            subprocess.call(cmd)        