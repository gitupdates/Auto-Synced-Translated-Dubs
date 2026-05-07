import typing
from dataclasses import dataclass, field

# Subtitle Dictionary Types
# These represent subtitle entries at various stages of processing

class CaptionSnippet(typing.TypedDict):
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

class Caption(typing.TypedDict):
    kind: str
    etag: str
    id: str
    snippet: CaptionSnippet

class CaptionListResponse(typing.TypedDict):
    kind: str
    etag: str
    items: typing.List[Caption]

class Boundary(typing.TypedDict):
    Text: str
    AudioOffset: int
    Duration: int

# Elevenlabs Alignment object type within response for timed text to speech
class EL_alignment(typing.TypedDict):
    characters: list[str]
    character_start_times_seconds: list[float]
    character_end_times_seconds: list[float]

# Response for timed text to speech request
class EL_TimedSpeechResponse(typing.TypedDict):
    audio_base64: str
    alignment: EL_alignment
    normalized_alignment: EL_alignment

@dataclass
class SubtitleEntry:
    # Core fields
    srt_timestamps_line: str = ''
    start_ms: int = -1
    end_ms: int = -1
    duration_ms: int = -1
    text: str = ''
    break_until_next: int = 0
    # Buffered timing
    start_ms_buffered: int = -1
    end_ms_buffered: int = -1
    duration_ms_buffered: int = -1
    # Translation fields
    translated_text: str = ''
    originalIndex: int = 0
    char_rate: float = 0.0
    char_rate_diff: float = 0.0
    force_split_at_start: int = 0
    force_split_at_end: int = 0
    # TTS fields
    TTS_FilePath: str = ''
    TTS_Word_Boundaries: list['Boundary'] = field(default_factory=list)
    TTS_Sentence_Boundaries: list['Boundary'] = field(default_factory=list)
    # Audio processing
    TTS_FilePath_Trimmed: str = ''
    speed_factor: float = 1.0
    start_trimmed_ms: int = 0
    end_trimmed_ms: int = 0

# Integer-keyed dictionary of subtitle entries (after index conversion)
SubtitleDict = dict[int, SubtitleEntry]