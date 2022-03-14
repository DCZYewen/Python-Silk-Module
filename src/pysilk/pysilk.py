import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from os import cpu_count
from typing import Union, BinaryIO

from .coder import silkEncode, silkDecode
from .utils import get_file, is_silk_data
from .wav import Wave

_LOOP = asyncio.get_event_loop()
_EXECUTOR = ThreadPoolExecutor(cpu_count())


def encode(data: bytes, *, sample_rate=24000) -> bytes:
    if data[8:12] == b"WAVE":
        return silkEncode(
            Wave.wav2pcm(BytesIO(data)), sample_rate
        )
    return silkEncode(data, sample_rate)


def encode_file(target: Union[str, BinaryIO], *, sample_rate=24000) -> bytes:
    fd = get_file(target)
    try:
        return encode(fd.read(), sample_rate=sample_rate)
    finally:
        fd.close()


def decode(silk_data: bytes, to_wav=False, *, sample_rate=24000) -> bytes:
    if is_silk_data(silk_data):
        if not to_wav:
            return silkDecode(silk_data, sample_rate)
        else:
            return Wave.pcm2wav(
                BytesIO(silkDecode(silk_data, sample_rate))
            )
    else:
        raise ValueError("Not a valid silk_data")


def decode_file(silk_file: Union[str, BinaryIO], to_wav=False, *, sample_rate=24000) -> bytes:
    fd = get_file(silk_file)
    try:
        return decode(fd.read(), to_wav, sample_rate=sample_rate)
    finally:
        fd.close()


async def async_encode(data: bytes, *, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, functools.partial(encode, data, sample_rate=sample_rate))


async def async_decode(silk_data: bytes, to_wav=False, *, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(
        _EXECUTOR, functools.partial(decode, silk_data, sample_rate=sample_rate, to_wav=to_wav)
    )


async def async_encode_file(target: Union[str, BinaryIO], *, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, functools.partial(encode_file, target, sample_rate=sample_rate))


async def async_decode_file(silk_file: Union[str, BinaryIO], to_wav=False, *, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(
        _EXECUTOR, functools.partial(decode_file, silk_file, sample_rate=sample_rate, to_wav=to_wav)
    )
