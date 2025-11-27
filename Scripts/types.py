from typing import TypedDict, List


# Subtitle Dictionary Types
# These represent subtitle entries at various stages of processing
# Note: Using dict[str, Any] instead of TypedDict because keys are SubsDictKeys enum values,
# not literal strings, which TypedDict doesn't support well

# Type alias for a single subtitle entry
# The dictionary values can be str, int, or float depending on the field
SubtitleEntry = dict[str, str | int | float]

# Dictionary types for different key types
# Keys can be either str (line numbers as strings) or int (after conversion)
SubtitleDict = dict[str, SubtitleEntry]  # String keys (line numbers as strings like "1", "2", etc.)
SubtitleDictInt = dict[int, SubtitleEntry]  # Integer keys (after conversion to int)

"""
Subtitle Entry Fields (accessed via SubsDictKeys enum):
    
Core fields (always present after parsing):
    - start_ms: str - Start time in milliseconds
    - end_ms: str - End time in milliseconds  
    - duration_ms: str - Duration in milliseconds
    - text: str - Original subtitle text
    - break_until_next: int | str - Time gap until next subtitle in ms
    - srt_timestamps_line: str - Original SRT timestamp line (e.g., "00:00:20,130 --> 00:00:23,419")
    
Buffered timing fields (added during parsing if buffer is applied):
    - start_ms_buffered: str
    - end_ms_buffered: str
    - duration_ms_buffered: str
    
Translation fields (added after translation):
    - translated_text: str - Translated text
    - originalIndex: int - Original index before combination
    - char_rate: float | str - Characters per second rate
    - char_rate_diff: float - Difference from target char rate
    
TTS fields (added after synthesis):
    - TTS_FilePath: str - Path to synthesized audio file
    - speed_factor: float - Speed adjustment factor for audio
    
Audio processing fields (added during audio building):
    - TTS_FilePath_Trimmed: str - Path to trimmed audio file
"""


class CaptionSnippet(TypedDict):
    videoId: str
    lastUpdated: str
    trackKind: str
    language: str
    name: str
    audioTrackType: str
    isCC: bool
    isLarge: bool
    isEasyReader: bool
    isDraft: bool
    isAutoSynced: bool
    status: str

class Caption(TypedDict):
    kind: str
    etag: str
    id: str
    snippet: CaptionSnippet

class CaptionListResponse(TypedDict):
    kind: str
    etag: str
    items: List[Caption]
