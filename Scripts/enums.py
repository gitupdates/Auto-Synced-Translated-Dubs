#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import enum

class TranslateService(str, enum.Enum):
    GOOGLE = "google"
    DEEPL = "deepl"

    def __str__(self):
        return self.value
    
class GoogleTranslateMode(str, enum.Enum):
    NMT = "nmt",
    LLM = "llm"

class TTSService(str, enum.Enum):
    AZURE = "azure"
    GOOGLE = "google"
    ELEVENLABS = "elevenlabs"
    
    def __str__(self):
        return self.value

# Cloud services that need a dedicated authenticated object
class AuthCloudServices(enum.Enum):
    GOOGLE = "google"
    DEEPL = "deepl"
    YOUTUBE = "youtube"

class AudioFormat(str, enum.Enum):
    MP3 = "mp3"
    AAC = "aac"
    WAV = "wav"
    
    def __str__(self):
        return self.value

class AudioStretchMethod(str, enum.Enum):
    FFMPEG = "ffmpeg"
    RUBBERBAND = "rubberband"
    
    def __str__(self):
        return self.value

class ElevenLabsModel(str, enum.Enum):
    MONOLINGUAL_V1 = "eleven_monolingual_v1"
    MULTILINGUAL_V2 = "eleven_multilingual_v2"
    DEFAULT = "default"
    
    def __str__(self):
        return self.value

class FormalityPreference(str, enum.Enum):
    DEFAULT = "default"
    MORE = "more"
    LESS = "less"
    
    def __str__(self):
        return self.value
    
class LangDataKeys(str, enum.Enum):
    translation_target_language = "translation_target_language"
    synth_voice_name = "synth_voice_name"
    synth_language_code = "synth_language_code"
    synth_voice_gender = "synth_voice_gender"
    translate_service = "translate_service"
    formality = "formality"
    synth_voice_model = "synth_voice_model"
    synth_voice_style = "synth_voice_style"
    
    def __str__(self) -> str:
        return self.value
    
class LangDictKeys(str, enum.Enum):
    targetLanguage = "targetLanguage"
    voiceName = "voiceName"
    languageCode = "languageCode"
    voiceGender = "voiceGender"
    translateService = "translateService"
    formality = "formality"
    voiceModel = "voiceModel"
    voiceStyle = "voiceStyle"
    
    def __str__(self):
        return self.value
    
class SubsDictKeys(str, enum.Enum):
    start_ms = "start_ms"
    end_ms = "end_ms"
    duration_ms = "duration_ms"
    text = "text"
    break_until_next = "break_until_next"
    srt_timestamps_line = "srt_timestamps_line"
    start_ms_buffered = "start_ms_buffered"
    end_ms_buffered = "end_ms_buffered"
    duration_ms_buffered = "duration_ms_buffered"
    translated_text = "translated_text"
    originalIndex = "originalIndex"
    char_rate = "char_rate"
    char_rate_diff = "char_rate_diff"
    TTS_FilePath = "TTS_FilePath"
    TTS_FilePath_Trimmed = "TTS_FilePath_Trimmed"
    speed_factor = "speed_factor"
    force_split_at_start = "force_split_at_start"
    force_split_at_end = "force_split_at_end"

    def __str__(self):
        return self.value
    
class VariousDefaults():
    defaultSpeechRateGoal:float = 20

