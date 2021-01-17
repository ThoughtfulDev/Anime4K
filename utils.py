from shutil import which
import os

def credz():
    print("___________________________________")
    print("   _        _           _ _  _  __")
    print("  /_\  _ _ (_)_ __  ___| | || |/ /")
    print(" / _ \| ' \| | '  \/ -_)_  _| ' < ")
    print("/_/ \_\_||_|_|_|_|_\___| |_||_|\_\\")
    print("___________________________________")
    print("    Upscale your Favorite Anime!   ")
    print("       Made by ThoughtfulDev       ")
    print("\n")
                                   

def is_tool(name):
    return which(name) is not None

def langToShort(lang):
    if lang == 'English':
        return "eng"
    elif lang == 'Japanese':
        return "jpn"
    else:
        return "und"

def shortToLong(lang):
    if lang == "eng":
        return "English"
    elif lang == "jpn" or lang == "jap" or lang == "ja":
        return "Japanese"
    elif lang == "fra":
        return "French"
    else:
        return "Unknown"

language_mapping = {
    "eng": "English",
    "ja": "Japanese",
    "jp": "Japanese",
    "jap": "Japanese",
    "jpn": "Japanese",
    "ger": "German",
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')