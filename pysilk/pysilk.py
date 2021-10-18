import asyncio

from os import cpu_count
from typing import Union, BinaryIO
from concurrent.futures import ThreadPoolExecutor

from _pysilk import silkEncode, silkDecode
from .utils import get_file, is_silk_data


_LOOP = asyncio.get_event_loop()
_EXECUTOR = ThreadPoolExecutor(cpu_count())


def encode(pcm_data: bytes, sample_rate=24000) -> bytes:
    return silkEncode(pcm_data, sample_rate)


def encode_file(pcm_file: Union[str, BinaryIO], sample_rate=24000) -> bytes:
    # TODO: wav format support
    fd = get_file(pcm_file)
    try:
        return encode(fd.read(), sample_rate)
    finally:
        fd.close()


def decode(silk_data: bytes, sample_rate=24000) -> bytes:
    if is_silk_data(silk_data):
        return silkDecode(silk_data, sample_rate)
    else:
        raise ValueError("Not a valid silk_data")


def decode_file(silk_file: Union[str, BinaryIO], sample_rate=24000) -> bytes:
    fd = get_file(silk_file)
    try:
        return decode(fd.read(), sample_rate)
    finally:
        fd.close()


async def async_encode(pcm_data: bytes, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, encode, pcm_data, sample_rate)


async def async_decode(silk_data: bytes, sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, decode, silk_data, sample_rate)


async def async_encode_file(pcm_file: Union[str, BinaryIO], sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, encode_file, pcm_file, sample_rate)


async def async_decode_file(silk_file: Union[str, BinaryIO], sample_rate=24000) -> bytes:
    return await _LOOP.run_in_executor(_EXECUTOR, decode_file, silk_file, sample_rate)
