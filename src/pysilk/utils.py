import sys
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


def force_quit():
    import os
    import multiprocessing
    os.kill(multiprocessing.current_process().pid, 15)  # sigterm


def _play_sound(source: Union[str, bytes]):
    import winsound
    from threading import Thread

    t = Thread(
        target=winsound.PlaySound,
        name="PlayerThread",
        args=(source, winsound.SND_FILENAME if isinstance(source, str) else winsound.SND_MEMORY),
    )
    t.start()
    try:
        while True:
            t.join(0.5)
    except KeyboardInterrupt:
        print("Interrupt received")
        force_quit()


def play_audio(source: Union[str, bytes]):
    if sys.platform != "win32":
        raise RuntimeError("PlaySound only support windows")

    _play_sound(source)
