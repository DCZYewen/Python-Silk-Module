from typing import Union, BinaryIO

from _pysilk import silkEncode, silkDecode
from .utils import get_file, is_silk_data


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
        return encode(fd.read(), sample_rate)
    finally:
        fd.close()
