from consts import GUI_OPTS
import PySimpleGUI as sg
import threading
import sys, os
import argparse, subprocess
import select
from utils import is_tool, credz, str2bool
from extract_audio import extract_audio
from extract_subs import extract_subs
from mux import mux
from shader import shader
from encode import encode_to_hevc
from splitter import split_by_seconds, get_video_length

DEFAULT_VARS = {
    "THEME": "DarkGrey10"
}

PROC_THREAD = None

UPSCALE_FINISHED = False
UPSCALE_RUNNING = False

ENCODE_FINISHED = False
ENCODE_RUNNING = False

AUDIO_FINISHED = False
AUDIO_RUNNING = False

def make_window(theme):
    sg.theme(theme)

    upscale_layout = [
        [sg.Text("Choose a input file")],
        [
            sg.Input(key='upscale_input_inputfilename', enable_events=True, readonly=True), 
            sg.FileBrowse()
        ],
        [sg.Text("Choose if you input file is 10bit: "), sg.Checkbox('Yes', default=False, key='upscale_checkbox_10bit')],
        [sg.T('', font='any 1')],
        [sg.Text("Choose your shader directory")],
        [
            sg.Input(key='upscale_input_shaderdir', enable_events=True, readonly=True), 
            sg.FolderBrowse()
        ],
        [sg.T('', font='any 1')],
        [
            sg.Text("Width (in px):"),
            sg.Input(key='upscale_input_width', default_text="3840", size=(7,)), 
            sg.Text("Height (in px):"),
            sg.Input(key='upscale_input_height', default_text="2160",size=(7,))
        ],
        [sg.T('', font='any 1')],
        [sg.Text('Quality and Mode Options:')],
        [sg.Text("Choose what to use when encoding after applying shaders:")],
        [
            sg.Combo(values=[
                'CPU (only x264 4:4:4) - needs to be converted to x265 later', 
                'GPU (NVENC HEVC/X265 - NVIDIA ONLY - no conversation necessary'
                ], key='upscale_combo_cg_choice')
        ],
        [sg.Text("Choose your Option for the Shader Mode:")],
        [
            sg.Combo(values=[
                'Remain as faithful to the original while enhancing details', 
                'Improve perceptual quality',
                'Improve perceptual quality + deblur'
                ], key='upscale_combo_shader_mode_choice')
        ],
        [sg.T('', font='any 1')],
        [sg.Text("Choose a Quality preset for encoding. \n\nThis will influence the shaders used but no the encoding preset itself:")],
        [
            sg.Combo(values=[
                'Fast', 
                'Medium',
                'Make my GPU hurt'
                ], key='upscale_combo_shader_quality_choice')
        ],
        [sg.T('', font='any 1')],
        [sg.Text("Please choose your Bilateral Denoise Mode:")],
        [
            sg.Combo(values=[
                'Mode (not so heavy)', 
                '[Recommended] Median (heavier)'
                ], key='upscale_combo_shader_bilateral_choice')
        ],
        [sg.T('', font='any 1')],
        [sg.Text("Specify your x264 Options")],
        [sg.Text("x264 preset"), sg.Combo(values=["veryfast", "fast", "medium", "slow", "veryslow"], key='upscale_combo_x264_preset')],
        [sg.Text("x264 lossless"), sg.Checkbox('Yes', default=False, key='upscale_checkbox_x264_lossless')],
        
        [sg.T('', font='any 1')],
        [sg.Text("Output file")],
        [sg.Input(key='upscale_input_outputfilename', enable_events=True, readonly=False)],


        [sg.Button("Upscale", key="upscale_btn_confirm")]
    ]

    encoding_layout = [
        [sg.Text("Choose a input file")],
        [
            sg.Input(key='encoding_input_inputfilename', enable_events=True, readonly=True), 
            sg.FileBrowse()
        ],
        [sg.Text("Output file")],
        [sg.Input(key='encoding_input_outputfilename', enable_events=True, readonly=False)],
        [sg.Text("Please choose your Encoding Preset:")],
        [
            sg.Combo(values=[
                "(Recommended if you dont know) One Setting to rule them all",
                "(e.g Your Name) Flat, slow anime (slice of life, everything is well lit)",
                "(e.g Kimetsu no Yaiba) Some dark scene, some battle scene (shonen, historical, etc.)",
                "(Rarely used) [TV Series] Movie-tier dark scene, complex grain/detail",
                "(Rarely used) [Movie] Movie-tier dark scene, complex grain/detail"
                ], key='encoding_combo_mode')
        ],
        [sg.Button("Encode", key="encode_btn_confirm")]
    ]

    layout = [
        [sg.TabGroup([
            [sg.Tab('Upscale', upscale_layout)],
            [sg.Tab('Encode', encoding_layout)]
        ])],
        [sg.Text("Status: N/A", key="label_status", size=(30,10))]
    ]
    return sg.Window("Anime4K", layout, font=("Arial", 11))

def upscale(values):
    global UPSCALE_FINISHED
    fn = values['upscale_input_inputfilename']
    bit = True if values['upscale_checkbox_10bit'] == 1 else False
    shader_dir = values['upscale_input_shaderdir']
    width = int(values['upscale_input_width'])
    height = int(values['upscale_input_height'])

    cg_combo_choice = values['upscale_combo_cg_choice']
    if "CPU" in cg_combo_choice: cg_choice = 0
    elif "GPU" in cg_combo_choice: cg_choice = 1
    else: cg_choice = 0

    mode_combo_choice = values['upscale_combo_shader_mode_choice']
    if "faithful" in mode_combo_choice:
        shader_mode_choice = 0
    elif mode_combo_choice == "Improve perceptual quality":
        shader_mode_choice = 1
    elif "deblur" in mode_combo_choice:
        shader_mode_choice = 2
    else:
        shader_mode_choice = 2
    
    quality_encode_choice = values['upscale_combo_shader_quality_choice']
    if quality_encode_choice == "Fast":
        shader_quality_choice = 0
    elif quality_encode_choice == "Medium":
        shader_quality_choice = 1
    elif quality_encode_choice == "Make my GPU hurt":
        shader_quality_choice = 2
    else:
        shader_quality_choice = 2
    
    combo_bi_choice = values['upscale_combo_shader_bilateral_choice']
    if "Mode" in combo_bi_choice:
        shader_bilateral_choice = 0
    elif "heavier" in combo_bi_choice:
        shader_bilateral_choice = 1
    else:
        shader_bilateral_choice = 1
    
    x264_preset = values['upscale_combo_x264_preset'] if values['upscale_combo_x264_preset'] != '' else 'medium'
    x264_lossless = int(values['upscale_checkbox_x264_lossless'])

    opts = GUI_OPTS
    opts['upscale']['width'] = width
    opts['upscale']['height'] = height
    opts['upscale']['cg_choice'] = cg_choice
    opts['upscale']['shader_mode_choice'] = shader_mode_choice
    opts['upscale']['shader_quality_choice'] = shader_quality_choice
    opts['upscale']['shader_bilateral_choice'] = shader_bilateral_choice
    opts['upscale']['x264_preset'] = x264_preset
    opts['upscale']['x264_lossless'] = x264_lossless
    
    outname = values['upscale_input_outputfilename']

    shader(fn, width, height, shader_dir, bit, outname, gui=True, opts=opts)
    UPSCALE_FINISHED = True


def encode(values):
    global ENCODE_FINISHED
    input = values['encoding_input_inputfilename']
    output = values['encoding_input_outputfilename']
    mode = values['encoding_combo_mode']
    opts = GUI_OPTS
    mode_int = 0
    if "Recommended" in mode:
        mode_int = 0
    elif "Your Name" in mode:
        mode_int = 1
    elif "Kimetsu no Yaiba" in mode:
        mode_int = 2
    elif "[TV Series]" in mode:
        mode_int = 3
    elif "[Movie]" in mode:
        mode_int = 4
    else:
        #default to recommended
        mode_int = 0

    opts['encode']['mode'] = mode_int
    encode_to_hevc(input, output, opts=opts)
    ENCODE_FINISHED = True

def thread_upscale(values):
    global PROC_THREAD
    global UPSCALE_RUNNING
    PROC_THREAD = threading.Thread(target=upscale, args=[values])
    UPSCALE_RUNNING = True
    PROC_THREAD.start()

def thread_encode(values):
    global PROC_THREAD
    global ENCODE_RUNNING
    PROC_THREAD = threading.Thread(target=encode, args=[values])
    ENCODE_RUNNING = True
    PROC_THREAD.start()


    

def main():
    global PROC_THREAD
    global UPSCALE_FINISHED, UPSCALE_RUNNING
    global ENCODE_FINISHED, ENCODE_RUNNING
    global AUDIO_FINISHED, AUDIO_RUNNING

    window = make_window(DEFAULT_VARS['THEME'])

   

    while True:
        event, values = window.read(timeout=100)
        # check the running threads
        if PROC_THREAD != None and UPSCALE_FINISHED == True:
            sg.popup("Finished Upscaling")
            UPSCALE_FINISHED = False
            UPSCALE_RUNNING = False
            PROC_THREAD = None
            window["label_status"].update("Status: Stopped")

        elif PROC_THREAD != None and ENCODE_FINISHED == True:
            sg.popup("Finished Encoding")
            ENCODE_FINISHED = False
            ENCODE_RUNNING = False
            PROC_THREAD = None
            window["label_status"].update("Status: Stopped")

        elif PROC_THREAD != None and AUDIO_FINISHED == True:
            sg.popup("Finished Audio Extract")
            AUDIO_FINISHED = False
            AUDIO_RUNNING = False
            PROC_THREAD = None
            window["label_status"].update("Status: Stopped")

        if event == sg.WIN_CLOSED:
            break
        elif event == "upscale_btn_confirm":
            window["label_status"].update("Status: Upscaling running...")
            thread_upscale(values)    
        elif event == "encode_btn_confirm":
            window["label_status"].update("Status: Encoding running...")
            thread_encode(values)

    if PROC_THREAD != None:
        PROC_THREAD.join()

    window.close()
    exit(0)

if __name__ == '__main__':
    main()