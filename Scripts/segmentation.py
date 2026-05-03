#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Imports
from Scripts.shared_imports import *

from typing import Optional, cast
import pathlib

def reflow_subtitles(subsDict: SubtitleDict, langCode:str, langName:str, doOutputFile:Optional[bool]=True, outFilePath:Optional[str]=None) -> tuple[str, str]|None:
    # Wordboundary / sentence boundary object contains list of objects looking like the below. We will use this info to create a new subtitle file such that it syncs with the audio.
        #   {
        #     "Text": "The",
        #     "AudioOffset": 50,    <- milliseconds relative to start of that segment's audio
        #     "Duration": 137       <- milliseconds
        #   },

    # Determine output path
    if outFilePath is None:
        output_path = pathlib.Path(ORIGINAL_VIDEO_PATH).stem + f" - {langName} - {langCode}.srt"
    else:
        output_path = outFilePath

    # First we need to combine all the boundaries. They'll be created per individual audio file, not the whole, so we need to account for that.
    all_boundaries: list[dict] = []
    
    # Sort the segments by ID to process them sequentially. 
    # DO NOT sort `all_boundaries` globally by start_ms afterwards, because audio segments often 
    # overlap (e.g. trailing silence) and global sorting will interleave words from different sentences.
    sorted_segments = sorted(subsDict.items(), key=lambda item: int(item[0]))

    for id, segment in sorted_segments:
        # Try to get the TTS_Word_Boundaries key in the object
        word_boundaries = cast(list[Boundary], segment.get(SubsDictKeys.TTS_Word_Boundaries, []))

        # If they exist, add the segment's start time to the offsets and add them to the all_boundaries list
        segment_start_ms = int(cast(str | int | float, segment[SubsDictKeys.start_ms]))
        
        full_text = str(segment.get("translated_text") or segment.get("text", ""))
        current_pos = 0
        segment_boundaries: list[dict] = []

        for boundary in word_boundaries:
            b_text = boundary["Text"]
            b_start = segment_start_ms + int(boundary["AudioOffset"])
            b_dur = int(boundary["Duration"])

            idx = full_text.find(b_text, current_pos)
            
            if idx != -1:
                chars_skipped = full_text[current_pos:idx]
                
                # Catch any words/formatting the TTS completely skipped over
                skipped_text = chars_skipped.strip()
                if skipped_text:
                    if segment_boundaries:
                        # If in the middle, attach to the previous token
                        segment_boundaries[-1]["text"] += " " + skipped_text
                    else:
                        # If at the very beginning, prepend to the current token
                        b_text = skipped_text + " " + b_text
                
                # If we skipped absolutely nothing, the token touches the previous one without spaces, so they merge.
                if chars_skipped == "" and segment_boundaries:
                    last_b = segment_boundaries[-1]
                    last_b["text"] += b_text
                    end_time = max(last_b["start_ms"] + last_b["duration_ms"], b_start + b_dur)
                    last_b["duration_ms"] = end_time - last_b["start_ms"]
                else:
                    segment_boundaries.append({
                        "text": b_text,
                        "start_ms": b_start,
                        "duration_ms": b_dur
                    })
                current_pos = idx + len(boundary["Text"])
            else:
                # Fallback: if token isn't found in the text, assume it's hallucinated formatting.
                # If it's punctuation, we merge it to the last word. Otherwise, treat as new.
                if not b_text.isalnum() and segment_boundaries:
                    last_b = segment_boundaries[-1]
                    last_b["text"] += b_text
                    end_time = max(last_b["start_ms"] + last_b["duration_ms"], b_start + b_dur)
                    last_b["duration_ms"] = end_time - last_b["start_ms"]
                else:
                    segment_boundaries.append({
                        "text": b_text,
                        "start_ms": b_start,
                        "duration_ms": b_dur
                    })

        # Catch any trailing text that the TTS missed at the very end of the segment (like "[fin]")
        trailing_text = full_text[current_pos:].strip()
        if trailing_text:
            if segment_boundaries:
                segment_boundaries[-1]["text"] += " " + trailing_text
            else:
                # If there were no valid boundaries at all but there is text, create a fallback token
                segment_dur = int(cast(str | int | float, segment.get("duration_ms", 0)))
                segment_boundaries.append({
                    "text": trailing_text,
                    "start_ms": segment_start_ms,
                    "duration_ms": segment_dur
                })

        all_boundaries.extend(segment_boundaries)

    if not all_boundaries:
        print(f"  > WARNING: [Lang: {langCode}] No word boundaries found in TTS data. Cannot create reflowed SRT subtitles. The voice for this language may not support word boundaries.")
        return None

    # Group words into subtitle entries targeting 2 lines of ~42 chars each
    MAX_CHARS_PER_LINE = 42
    MAX_CHARS = MAX_CHARS_PER_LINE * 2

    subtitle_groups: list[list[dict]] = []
    current_group: list[dict] = []
    current_len = 0

    for boundary in all_boundaries:
        word = boundary["text"]
        add_len = len(word) + (1 if current_group else 0)  # +1 for space separator

        if current_group and current_len + add_len > MAX_CHARS:
            subtitle_groups.append(current_group)
            current_group = [boundary]
            current_len = len(word)
        else:
            current_group.append(boundary)
            current_len += add_len

    if current_group:
        subtitle_groups.append(current_group)

    # Helper: convert milliseconds to SRT timestamp string
    def ms_to_srt(ms: int) -> str:
        ms = max(0, ms)
        h = ms // 3600000; ms %= 3600000
        m = ms // 60000;   ms %= 60000
        s = ms // 1000;    ms %= 1000
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    # Helper: wrap a group of word dicts into lines of at most max_line_chars
    def wrap_words(words: list[dict], max_line_chars: int) -> str:
        lines: list[str] = []
        line_words: list[str] = []
        line_len = 0
        for w in words:
            word = w["text"]
            add = len(word) + (1 if line_words else 0)
            if line_words and line_len + add > max_line_chars:
                lines.append(' '.join(line_words))
                line_words = [word]
                line_len = len(word)
            else:
                line_words.append(word)
                line_len += add
        if line_words:
            lines.append(' '.join(line_words))
        return '\n'.join(lines)
    
    finalFullSrtContents:str = ""
    reflowed_transcript:str = "" # To compare original text to reflowed to ensure punctuation was correct
    
    for i, group in enumerate(subtitle_groups, 1):
        start_ms = group[0]["start_ms"]
        end_ms = group[-1]["start_ms"] + group[-1]["duration_ms"]
        
        # Ensure SRT times don't overlap if audio segments overlapped
        if i < len(subtitle_groups):
            next_start = subtitle_groups[i][0]["start_ms"]
            if end_ms > next_start:
                end_ms = max(start_ms, next_start - 1)
                
        text = wrap_words(group, MAX_CHARS_PER_LINE)
        finalFullSrtContents += f"{i}\n{ms_to_srt(start_ms)} --> {ms_to_srt(end_ms)}\n{text}\n\n"
        reflowed_transcript += text.replace('\n', ' ') + " "

    # Write the file
    if doOutputFile == True:
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(finalFullSrtContents)
    
    # Determine the original full transcript to compare and ensure it's identical, if not warn the user
    originalFullTranscript:str = ""
    for i, obj in subsDict.items():
        currSegmentText:str = f"{obj['translated_text']} "
        originalFullTranscript += currSegmentText

    if originalFullTranscript.strip() != reflowed_transcript.strip():
        originalTranscriptFileName:str = f"{ORIGINAL_VIDEO_NAME}_{langCode}_original_transcript.txt"
        reflowedlTranscriptFileName:str = f"{ORIGINAL_VIDEO_NAME}_{langCode}_reflowed_transcript.txt"
        
        error_msg:str = f"  > WARNING: [Lang: {langCode}] Reflowed subtitle text does not perfectly match the original translation, inspect the difference in case something went wrong."
        error_msg += f"Will output the original and reflowed transcripts to compare as:\n    {originalTranscriptFileName}\n    {reflowedlTranscriptFileName}"
        print(error_msg)
        
        with open(os.path.join(OUTPUT_FOLDER, originalTranscriptFileName), 'w', encoding='utf-8-sig') as f:
            f.write(originalFullTranscript)
        with open(os.path.join(OUTPUT_FOLDER, reflowedlTranscriptFileName), 'w', encoding='utf-8-sig') as f:
            f.write(reflowed_transcript)
    
    return finalFullSrtContents, reflowed_transcript