from enum import Enum
from io import BytesIO


class AudioCodec(Enum):
    SIRENSR = 1
    GSM610 = 2


class AudioChannels(Enum):
    MONO = 1


class SpeechboxAudio:
    def __init__(self) -> None:
        self.io: BytesIO = BytesIO()

        self._codec: AudioCodec = 0
        self._sampling_rate: int = None
        self._channels: AudioChannels = 0

    def __repr__(self) -> str:
        return '{}(codec={!r}, sampling_rate={!r}, channels={!r})'.format(
            self.__class__.__name__,
            self.codec,
            self.sampling_rate,
            self.channels,
        )

    @property
    def codec(self) -> AudioCodec:
        return self._codec

    @property
    def sampling_rate(self) -> int:
        return self._sampling_rate

    @property
    def channels(self) -> AudioChannels:
        return self._channels


class SpeechboxAudioGSM611(SpeechboxAudio):
    def __init__(self, codec: str, sampling_rate: int, channels: str) -> None:
        super().__init__()

        self._sampling_rate: int = sampling_rate

        codec_part = codec.split('/', 1)[1]
        if codec_part == 'gsm':
            self._codec = AudioCodec.GSM610
        else:
            raise ValueError('Audio codec can be only "audio/gsm"')

        if channels == 'mono':
            self._channels = AudioChannels.MONO
        else:
            raise ValueError('Audio channels can be only "mono"')


class SpeechboxAudioSirenSR(SpeechboxAudio):
    def __init__(self) -> None:
        super().__init__()

        self._codec = AudioCodec.SIRENSR
        self._sampling_rate = 16000
        self._channels = AudioChannels.MONO
