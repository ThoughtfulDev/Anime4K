import subprocess, os, sys
from pymediainfo import MediaInfo
from utils import clear
from simple_term_menu import TerminalMenu
from consts import *

x264_mapping = [
    "veryfast", "fast", "medium", "slow", "veryslow"
]

def FHDMenu(shader_dir):
    mode_menu = TerminalMenu(
        ["Remain as faithful to the original while enhancing details", 
        "Improve perceptual quality", 
        "Improve perceptual quality + deblur"
        ],
        title="Choose your Option for Full HD Videos"
    )
    mode_choice = mode_menu.show()


    quality_menu = TerminalMenu(
        [
            "Fast", "Medium", "Make my CPU and GPU hurt"
        ],
        title="Choose a Quality preset for encoding. This will influence the shaders used but no the encoding preset itself."
    )
    quality_choice = quality_menu.show()


    if mode_choice == None or quality_choice == None:
        print("Canceling")
        sys.exit(-1)

    #low quality
    if quality_choice == 0:
        if mode_choice == 0:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_M_x2_Deblur)
            return s
        elif mode_choice == 1:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_VeryFast)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_VeryFast)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_M_x2_Deblur)
            return s
        elif mode_choice == 2:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Deblur_DoG)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_VeryFast)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_VeryFast)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_M_x2_Deblur)
            return s
    # medium
    elif quality_choice == 1:
        if mode_choice == 0:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_L_x2_Deblur)
            return s
        elif mode_choice == 1:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_Fast)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_Fast)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_L_x2_Deblur)
            return s
        elif mode_choice == 2:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Deblur_DoG)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_Fast)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_Fast)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_L_x2_Deblur)
            return s
    #eat your gpu
    elif quality_choice == 2:
        if mode_choice == 0:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_UL_x2_Deblur)
            return s
        elif mode_choice == 1:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_HQ)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_HQ)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_UL_x2_Deblur)
            return s
        elif mode_choice == 2:
            s = os.path.join(shader_dir, Denoise_Bilateral_Mode)
            s = s + ":"
            s = s + os.path.join(shader_dir, Deblur_DoG)
            s = s + ":"
            s = s + os.path.join(shader_dir, DarkLines_HQ)
            s = s + ":"
            s = s + os.path.join(shader_dir, ThinLines_HQ)
            s = s + ":"
            s = s + os.path.join(shader_dir, Upscale_CNN_UL_x2_Deblur)
            return s

def lowerFHDMenu(shader_dir):
    pass

def shader(fn, width, height, shader, ten_bit, outname):
    '''print("Removing Audio and Subs from video.")
    subprocess.call([
        "ffmpeg",
        "-i",
        fn,
        "-c",
        "copy",
        "-sn",
        "-an",
        "-f",
        "matroska",
        "rem.mkv"
    ])'''
    clear()

    cg_menu = TerminalMenu(
        ["CPU (only x264 4:4:4) - needs to be converted to x265 later with ffmpeg", 
        "GPU (NVENC HEVC/X265 - may result in lower quality than CPU) - NVIDIA ONLY - no conversation necessary" 
        ],
        title="Choose what to use when encoding after applying shaders."
    )
    cg_choice = cg_menu.show()
    if cg_choice == 0:
        cpu_shader(fn, width, height, shader, ten_bit, outname)
    elif cg_choice == 1:
        gpu_shader(fn, width, height, shader, ten_bit, outname)
    else:
        print("Cancel")
        sys.exit(-2)


def gpu_shader(fn, width, height, shader, ten_bit, outname):
    clear()
    if ten_bit:
        print("File is 10Bit")
        format = "yuv420p10le"
    else:
        print("File is not 10Bit")
        format = "yuv420p"    
    
    #detect width and height of video.
    _m = MediaInfo.parse(fn)
    track_width = -1
    for t in _m.tracks:
        if t.track_type == 'Video':
            track_width = t.width
    
    clear()
    if int(track_width) >= 1920:
        str_shaders = FHDMenu(shader)
    else:
        str_shaders = lowerFHDMenu(shader)
    
    print("Using the following shaders:")
    print(str_shaders)
    print("Encoder: NVENC HEVC")
    import time
    time.sleep(3)
    clear()
    subprocess.call([
        "mpv",
        "--vf=format=" + format,
        fn,
        "--profile=gpu-hq",
        "--scale=ewa_lanczossharp",
        "--cscale=ewa_lanczossharp",
        "--video-sync=display-resample",
        "--interpolation",
        "--tscale=oversample",
        '--vf=gpu=w=' + str(width) + ':h=' + str(height),
        "--glsl-shaders=" + str_shaders,
        "--ovc=hevc_nvenc",
        '--ovcopts=rc=constqp:preset=1:profile=main10:rc-lookahead=32:qp=24',
        '--no-audio',
        '--o=' + outname
    ])

def cpu_shader(fn, width, height, shader, ten_bit, outname):
    clear()
    if ten_bit:
        print("File is 10Bit")
        format = "yuv420p10le"
    else:
        print("File is not 10Bit")
        format = "yuv420p"
    
    
    #detect width and height of video.
    _m = MediaInfo.parse(fn)
    track_width = -1
    for t in _m.tracks:
        if t.track_type == 'Video':
            track_width = t.width
    
    clear()
    if int(track_width) >= 1920:
        str_shaders = FHDMenu(shader)
    else:
        str_shaders = lowerFHDMenu(shader)
    

    
    
    x264_preset = x264_mapping[TerminalMenu(x264_mapping, title="Choose your x264 preset:").show()]

    lossless_menu = TerminalMenu(["No", "Yes"], title="Do you want to encode lossless? (Huge filesize)")
    lossless_choice = lossless_menu.show()
    if lossless_choice == 1:
        crf = 0
    else:
        crf = 17

    print("Using the following shaders:")
    print(str_shaders)
    print("Encoding with preset: " +  x264_preset)
    import time
    time.sleep(3)
    clear()

    
    subprocess.call([
        "mpv",
        "--vf=format=" + format,
        fn,
        "--profile=gpu-hq",
        "--scale=ewa_lanczossharp",
        "--cscale=ewa_lanczossharp",
        "--video-sync=display-resample",
        "--interpolation",
        "--tscale=oversample",
        '--vf=gpu=w=' + str(width) + ':h=' + str(height),
        "--glsl-shaders=" + str_shaders,
        "--ovc=libx264",
        '--ovcopts=preset=' + x264_preset + ':level=6.1:crf=' + str(crf) + ':aq-mode=3:psy-rd=1.0:bf=6',
        '--no-audio',
        '--o=' + outname
    ])

    
    
