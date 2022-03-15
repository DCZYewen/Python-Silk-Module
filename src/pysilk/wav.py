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
            elif wav.getnchannels() == 1:
                while True:
                    bl = wav.readframes(512)
                    if bl:
                        res.write(bl)
                    else:
                        break
            else:
                channel_data = bytearray()
                while True:
                    frame = wav.readframes(1)
                    if frame:
                        channel_data.append(frame[0])
                    else:
                        break
                res.write(channel_data)
        return res.getvalue()
