import os
import asyncio

ROOT = "asserts"


def local_file(path: str) -> str:
    return os.path.join(__file__.rsplit(os.sep, 1)[0], ROOT, path)


def get_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()
