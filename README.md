![Logo of the project](demo.gif)

# Anime4K-PyWrapper
> Wrapper for [Anime4K](https://github.com/bloc97/Anime4K)

Makes it easy to encode a Anime using the MPV shaders with predefined encoding profiles!

## Installing / Getting started

What you need:
- Python 3.X
- mpv > 0.32
- ffmpeg
- mkvnixtool
- A dedicated GPU (no VM) [AMD/NVIDIA/Intel]

**Installing the necessary python libs**

```
pip3 install -r requirements.txt
```

### Initial Configuration

Download the latest shaders from [here](https://github.com/bloc97/Anime4K/releases) also download the extra denoise shaders from [here](https://github.com/bloc97/Anime4K/tree/master/glsl/3.1/Denoise).
Put them all into one folder for example called *shaders*

## Upscaling your first Anime!

Assuming your Anime Movie/Episode is called *input.mkv* and has a resolution of 1920x1080.
Now you want to upscale it to 4K (3840x2160).
Here is the commands you would run.

1. Encode the Video (to x264 and upscale it using the shader with the first Option [CPU])
```
python3 Anime4K.py -m shader --shader_dir "./shaders" --width 3840 --height 2160 -i input.mkv --output x264_upscale.mkv
```
2. Choose the option *CPU (only x264 4:4:4)...* (for this example)
3. Follow the dialogues - they should be pretty self explanatory
4. Your file should now be in *x264_upscale.mkv*
5. Now we need to encode the file to x265 10bit
```
python3 Anime4K.py -m encode -i x264_upscale.mkv --output x265_10bit.mkv
```
6. Choose your desired encoding preset.
7. The output file *x265_10bit.mkv* has no audio or subtitles we add them in the next step.
8. Extract the audio and subtitles from the original file
```
python3 Anime4K.py -m audio -i input.mkv
python3 Anime4K.py -m subs -i input.mkv
```
9. Now we have the audio files and subtitles in the current folder.
10. Now lets add them into the final output
```
python3 Anime4K.py -m mux -i x265_10bit.mkv -o input_upscaled_with_audio_and_subs.mkv
```


**Feel free to explore the other options of the program (or profiles) by typing**:
```
python3 Anime4K.py --help
```

## **[Optional]** Encoding ffmpeg progressbar
To get a overview of your current encoding ffmpeg of ffmpeg you may install the [ffmpeg-progressbar-cli](https://github.com/sidneys/ffmpeg-progressbar-cli)

```
npm install --global ffmpeg-progressbar-cli
```

*Don't worry the script will also work with normal ffmpeg.*


## Features

* Encode Videos with Anime4K shaders easily
* Encode using NVENC or CPU
* Extract Audio and subtitles automatically
* Predefined profiles for Anime4K and ffmpeg

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Links

- Related projects:
  - [**Huge thanks!**] Anime4K: https://github.com/bloc97/Anime4K
  - video2x: https://github.com/k4yt3x/video2x

- Thanks to:
  - ffmpeg-progressbar-cli: https://github.com/sidneys/ffmpeg-progressbar-cli
  - simple-term-menu: https://github.com/IngoHeimbach/simple-term-menu


## Licensing

The code in this project is licensed under GNU GENERAL PUBLIC LICENSE.
