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


@dataclass
class SubtitleEntry:
    # Core fields
    srt_timestamps_line: str = ''
    start_ms: str = ''
    end_ms: str = ''
    duration_ms: str = ''
    text: str = ''
    break_until_next: int = 0
    # Buffered timing
    start_ms_buffered: str = ''
    end_ms_buffered: str = ''
    duration_ms_buffered: str = ''
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