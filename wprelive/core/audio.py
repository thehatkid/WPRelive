from enum import IntEnum
from io import BytesIO

__all__ = (
    "AudioChannels",
    "SpeechboxAudio",
    "SpeechboxAudioGSM610",
    "SpeechboxAudioSirenSR",
)


class AudioChannels(IntEnum):
    """Speechbox audio channels enumeration."""

    MONO = 1


class SpeechboxAudio:
    """Represents an speechbox audio object.

    Attributes
    ----------
    io: :class:`BytesIO`
        The I/O buffered stream bytes.
    sampling_rate: :class:`int`
        The sampling rate of the audio.
    channels: :class:`.AudioChannels`
        The number of channels in the audio.
    """

    __slots__ = (
        "io",
        "_sampling_rate",
        "_channels",
    )

    def __init__(
        self,
        *,
        sampling_rate: int,
        channels: AudioChannels,
    ) -> None:
        self.io = BytesIO()
        self._sampling_rate = sampling_rate
        self._channels = channels

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"sampling_rate={self.sampling_rate!r} "
            f"channels={self.channels!r}>"
        )

    @property
    def sampling_rate(self) -> int:
        """:class:`int`: Returns sampling rate of the audio."""
        return self._sampling_rate

    @property
    def channels(self) -> AudioChannels:
        """:class:`int`: Returns channels number of the audio."""
        return self._channels


class SpeechboxAudioGSM610(SpeechboxAudio):
    """Represents an speechbox GSM 06.10 encoded audio.

    Attributes
    ----------
    io: :class:`BytesIO`
        The I/O buffered stream bytes.
    sampling_rate: :class:`int`
        The sampling rate of the audio.
    channels: :class:`.AudioChannels`
        The number of channels in the audio.
    """

    def __init__(self, codec: str, sampling_rate: int, channels: str) -> None:
        if codec.split("/", 1)[1] != "gsm":
            raise ValueError('Audio codec can be only "audio/gsm"')
        if channels != "mono":
            raise ValueError('Audio channels can be only "mono"')

        super().__init__(
            sampling_rate=sampling_rate,
            channels=AudioChannels.MONO,
        )


class SpeechboxAudioSirenSR(SpeechboxAudio):
    """Represents an speechbox SirenSR encoded audio.

    Attributes
    ----------
    io: :class:`BytesIO`
        The I/O buffered stream bytes.
    sampling_rate: :class:`int`
        The sampling rate of the audio.
    channels: :class:`.AudioChannels`
        The number of channels in the audio.
    """

    def __init__(self) -> None:
        super().__init__(
            sampling_rate=16000,
            channels=AudioChannels.MONO,
        )
