import asyncio
import os

ROOT = "assets"


def local_file(path: str) -> str:
    return os.path.join(__file__.rsplit(os.sep, 1)[0], ROOT, path)


def get_loop() -> asyncio.AbstractEventLoop:
    return asyncio.new_event_loop()
