from pathlib import Path
from typing import BinaryIO, Union


def is_silk_data(raw: bytes) -> bool:
    if len(raw) > 10:
        offset = 0
        if raw[0] == 2:
            offset = 1
        if raw[offset:10] == b"#!SILK_V3":
            return True
    return False


def get_file(file: Union[str, BinaryIO]) -> BinaryIO:
    if isinstance(file, str):
        path = Path(file)
        if not path.is_file():
            raise FileNotFoundError(file)
        return open(file, "rb")
    elif isinstance(file, BinaryIO):
        return file
    else:
        raise TypeError(file)
