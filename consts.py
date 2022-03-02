
Denoise_Bilateral_Mode = "Anime4K_Denoise_Bilateral_Mode.glsl"
Denoise_Bilateral_Median = "Anime4K_Denoise_Bilateral_Median.glsl"

DarkLines_VeryFast = "Anime4K_DarkLines_VeryFast.glsl"
DarkLines_Fast = "Anime4K_DarkLines_Fast.glsl"
DarkLines_HQ = "Anime4K_DarkLines_HQ.glsl"

ThinLines_VeryFast = "Anime4K_ThinLines_VeryFast.glsl"
ThinLines_Fast = "Anime4K_ThinLines_Fast.glsl"
ThinLines_HQ = "Anime4K_ThinLines_HQ.glsl"

Deblur_DoG = "Anime4K_Deblur_DoG.glsl"

Upscale_CNN_M_x2_Deblur = "Anime4K_Upscale_CNN_M_x2_Deblur.glsl"
Upscale_CNN_L_x2_Deblur = "Anime4K_Upscale_CNN_L_x2_Deblur.glsl"
Upscale_CNN_UL_x2_Deblur = "Anime4K_Upscale_CNN_UL_x2_Deblur.glsl"

Upscale_CNN_M_x2_Denoise = "Anime4K_Upscale_CNN_M_x2_Denoise.glsl"
Upscale_CNN_L_x2_Denoise = "Anime4K_Upscale_CNN_L_x2_Denoise.glsl"
Upscale_CNN_UL_x2_Denoise = "Anime4K_Upscale_CNN_UL_x2_Denoise.glsl"


Auto_Downscale_Pre_x4 = "Anime4K_Auto_Downscale_Pre_x4.glsl"

IS_GUI = False
GUI_OPTS = {
    "upscale": {
        "width": 3840,
        "height": 2160,
        "cg_choice": 0,
        "shader_mode_choice": 2,
        "shader_quality_choice": 2,
        "shader_bilateral_choice": 1,
        "x264_preset": "medium",
        "x264_lossless": 0
    },
    "encode": {
        "mode": 0
    },
    "audio": {

    }
}