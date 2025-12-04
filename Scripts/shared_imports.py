# pyright: reportConstantRedefinition=false
# pyright: reportUnusedImport=false

# Imports that won't be exported. Only needed 
import configparser

_EXPORT_START = set(globals().keys()) # This serves as a marker after which anything declared or imported will be exported

import os
import sys
import traceback 
import re
import regex
from typing import Any

# My Imports
from Scripts.utils import parseBool
from Scripts.load_configs import config, cloudConfig
from Scripts.enums import *
from Scripts.types import *

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


# Export anything in the global scope
__all__ = [name for name in globals() if name not in _EXPORT_START and not name.startswith('_')] # type: ignore[reportUnsupportedDunderAll]

