import asyncio
import functools
from pathlib import Path
from typing import BinaryIO, Union


def is_silk_data(raw: bytes) -> bool:
    if len(raw) > 10:
        if raw[:10] == b"\x02#!SILK_V3":
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


def run_async(func):
    loop = asyncio.get_event_loop()

    @functools.wraps(func)
    async def _run(*args, **kwargs):
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    return _run
