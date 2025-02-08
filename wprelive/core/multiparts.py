from email.message import Message
from typing import AsyncGenerator
from multipart import MultipartParser

from .audio import (
    SpeechboxAudio,
    SpeechboxAudioSirenSR,
    SpeechboxAudioGSM611,
)


def parse_options(value: str | bytes | None) -> tuple[str, dict[str, str]]:
    if not value:
        return ('', {},)

    if isinstance(value, bytes):
        value = value.decode()

    if ';' not in value:
        return (value, {},)

    value, extra = value.split(';', 1)

    message = Message()
    message['content-type'] = extra
    params = message.get_params()

    options: dict[str, str] = {}

    for param in params:
        k, v = param

        if isinstance(v, tuple):
            v = v[-1]

        if k == 'filename':
            if v[1:3] == ':\\' or v[:2] == '\\\\':
                v = v.split('\\')[-1]

        options[k] = v

    return (value, options,)


class SpeechboxMultipartParser:
    def __init__(
        self,
        stream: AsyncGenerator[bytes, None],
        boundary: bytes = b'WINDOWSPHONE-SPEECHBOX-BOUNDARY'
    ) -> None:
        self.stream: AsyncGenerator[bytes, None] = stream
        self.boundary: bytes = boundary
        self.audio: SpeechboxAudio = None

        self._end: bool = False

        self._headers: dict[str, str] = {}
        self._header_field: list[bytes] = []
        self._header_value: list[bytes] = []

        callbacks = {
            'on_part_data': self._on_part_data,
            'on_header_field': self._on_header_field,
            'on_header_value': self._on_header_value,
            'on_header_end': self._on_header_end,
            'on_headers_finished': self._on_headers_finished,
            'on_end': self._on_end,
        }
        self._parser = MultipartParser(self.boundary, callbacks)

    def __repr__(self) -> str:
        return '{}(audio={!r})'.format(self.__class__.__name__, self.audio)

    async def parse(self) -> SpeechboxAudio:
        async for chunk in self.stream:
            self._parser.write(chunk)

        return self.audio

    def _on_part_data(self, data: bytes, start: int, end: int) -> None:
        if self._end:
            return

        chunk = data[start:end]

        # Should be end of multipart
        if chunk == b'--' + self.boundary + b'--\r\n':
            self._on_end()
            return

        self.audio.io.write(chunk)

    def _on_header_field(self, data: bytes, start: int, end: int) -> None:
        self._header_field.append(data[start:end])

    def _on_header_value(self, data: bytes, start: int, end: int) -> None:
        self._header_value.append(data[start:end])

    def _on_header_end(self) -> None:
        field = b''.join(self._header_field).decode()
        value = b''.join(self._header_value).decode()
        self._headers[field] = value
        self._header_field.clear()
        self._header_value.clear()

    def _on_headers_finished(self) -> None:
        content_type = parse_options(self._headers['Content-Type'])
        mime = content_type[0]

        # Create SpeechboxAudio object
        if mime == 'audio/wav':
            codec = content_type[1]['codec']
            sampling_rate = int(content_type[1]['samplingrate'])
            channels = content_type[1]['channels']
            self.audio = SpeechboxAudioGSM611(codec, sampling_rate, channels)
        elif mime == 'audio/sirensr':
            self.audio = SpeechboxAudioSirenSR()
        else:
            raise ValueError('Supports only "audio/wav" and "audio/sirensr" audio MIME types')

    def _on_end(self) -> None:
        self._end = True
        self.audio.io.seek(0)
        self._parser.finalize()
        self._parser.close()
