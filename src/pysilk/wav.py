import itertools
import wave
from io import BytesIO
from typing import BinaryIO


class Wave:
    @staticmethod
    def pcm2wav(obj: BinaryIO, frame_rate=24000, *, ac=1) -> bytes:
        res = BytesIO()
        with wave.Wave_write(res) as wav:
            wav.setframerate(frame_rate)
            wav.setsampwidth(ac * 2)
            wav.setnchannels(ac)
            wav.writeframes(obj.read())
        return res.getvalue()

    @staticmethod
    def wav2pcm(obj: BinaryIO) -> bytes:
        res = BytesIO()
        with wave.Wave_read(obj) as wav:
            if wav.getcomptype() != "NONE":
                raise wave.Error("Unsupport with-compressed wave file")
            else:
                while True:
                    bl = wav.readframes(512)
                    if bl:
                        res.write(
                            bytearray(
                                [i for i in itertools.islice(bl, 0, 0, wav.getnchannels())]
                            )
                        )
                    else:
                        break
        return res.getvalue()
