import os
import sys
import traceback
import configparser
import re
import regex

from Scripts.utils import parseBool, parseConfigSetting
import Scripts.enums as enums
from Scripts.load_configs import config, cloudConfig

batchConfig = configparser.ConfigParser()
batchConfig.read('batch.ini') # Don't process this one, need sections in tact for languages
      
# ----- Validation Checks ------ (Add these to their own file eventually)
if config.skip_synthesize == True and cloudConfig.batch_tts_synthesize == True:
    raise ValueError(f'\nERROR: Cannot skip voice synthesis when batch mode is enabled. Please disable batch_tts_synthesize or set skip_synthesize to False.')
if cloudConfig.tts_service == "elevenlabs":
    if "yourkey" in cloudConfig.elevenlabs_api_key.lower():
        raise ValueError(f"\n\nERROR: You chose ElevenLabs as your TTS service, but didnt set your ElevenLabs API Key in cloud_service_settings.ini")

# ----- Create constants ------
ORIGINAL_VIDEO_PATH = batchConfig['SETTINGS']['original_video_file_path']
ORIGINAL_VIDEO_NAME = os.path.splitext(os.path.basename(ORIGINAL_VIDEO_PATH))[0]
OUTPUT_DIRECTORY = 'Outputs'
OUTPUT_YTSYNCED_DIRECTORY = 'YouTube Auto-Synced Subtitles'
OUTPUT_FOLDER = os.path.join(OUTPUT_DIRECTORY , ORIGINAL_VIDEO_NAME)
OUTPUT_YTSYNCED_FOLDER = os.path.join(OUTPUT_FOLDER, OUTPUT_YTSYNCED_DIRECTORY)

# Fix original video path if debug mode
if config.debug_mode and (ORIGINAL_VIDEO_PATH == '' or ORIGINAL_VIDEO_PATH.lower() == 'none'):
    ORIGINAL_VIDEO_PATH = 'Debug.test'
else:
    ORIGINAL_VIDEO_PATH = os.path.abspath(ORIGINAL_VIDEO_PATH.strip("\""))
    
# ------ Enums -------
TranslateService = enums.TranslateService
TTSService = enums.TTSService
AudioFormat = enums.AudioFormat
AudioStretchMethod = enums.AudioStretchMethod
ElevenLabsModel = enums.ElevenLabsModel
FormalityPreference = enums.FormalityPreference
LangDataKeys = enums.LangDataKeys
LangDictKeys = enums.LangDictKeys
SubsDictKeys = enums.SubsDictKeys
VariousDefaults = enums.VariousDefaults

# ---------------------------------------------------------------------------------------

# List of objects to export
exportObjects:list = [
    os,
    sys,
    traceback,
    config,
    cloudConfig,
    batchConfig,
    ORIGINAL_VIDEO_PATH,
    ORIGINAL_VIDEO_NAME,
    OUTPUT_DIRECTORY,
    OUTPUT_YTSYNCED_DIRECTORY,
    OUTPUT_FOLDER,
    OUTPUT_YTSYNCED_FOLDER,
    re,
    regex,
    parseBool,
    # Enums
    TranslateService,
    TTSService,
    AudioFormat,
    AudioStretchMethod,
    ElevenLabsModel,
    FormalityPreference,
    LangDataKeys,
    LangDictKeys,
    SubsDictKeys,
    VariousDefaults
]

# Export all objects
objNameList:list = []
for obj in exportObjects:
    strName = [name for name in globals() if globals()[name] is obj][0]
    objNameList.append(strName)

__all__ = objNameList # type: ignore[reportUnsupportedDunderAll]
