import wave
from io import BytesIO
from typing import BinaryIO


def pcm2wav(fobj: BinaryIO, frame_rate=24000, *, ac=1) -> bytes:
    res = BytesIO()
    with wave.Wave_write(res) as wav:
        wav.setframerate(frame_rate)
        wav.setsampwidth(ac * 2)
        wav.setnchannels(ac)
        for x in fobj:
            wav.writeframes(x)
    return res.getvalue()


def wav2pcm(fobj: BinaryIO) -> bytes:
    res = BytesIO()
    with wave.Wave_read(fobj) as wav:
        if wav.getcomptype() != "NONE":
            raise wave.Error("unsupport with-compress wave file")
        while True:
            # TODO: to_single_channel
            bl = wav.readframes(512)
            if bl:
                res.write(bl)
            else:
                break
    return res.getvalue()
