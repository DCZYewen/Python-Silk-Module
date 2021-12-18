import pytest
from io import BytesIO
from wave import Wave_read

from utils import local_file, get_loop

SILK_PATH = local_file("target.silk")
EXPECT_DATA = open(local_file("output.pcm"), "rb").read()[:30]
LOOP = get_loop()


def sync_decode(path: str, to_wav=False):
    from pysilk import decode

    with open(path, "rb") as f:
        return decode(f.read(), to_wav=to_wav)


def sync_decode_file(path: str, to_wav=False):
    from pysilk import decode_file

    return decode_file(path, to_wav=to_wav)


async def async_decode(path: str, to_wav=False):
    from pysilk import async_decode

    with open(path, "rb") as f:
        return await async_decode(f.read(), to_wav=to_wav)


async def async_decode_file(path: str, to_wav=False):
    from pysilk import async_decode_file

    return await async_decode_file(path, to_wav=to_wav)


class TestDecode:
    @pytest.mark.pcm
    @pytest.mark.sync
    @pytest.mark.decoder
    def test_sync_decode_pcm(self):
        assert sync_decode(SILK_PATH)[:30] == EXPECT_DATA

    @pytest.mark.pcm
    @pytest.mark.sync
    @pytest.mark.decoder
    def test_sync_decode_file_pcm(self):
        assert sync_decode_file(SILK_PATH)[:30] == EXPECT_DATA

    @pytest.mark.pcm
    @pytest.mark.async_
    @pytest.mark.decoder
    def test_async_decode_pcm(self):
        assert LOOP.run_until_complete(async_decode(SILK_PATH))[:30] == EXPECT_DATA

    @pytest.mark.pcm
    @pytest.mark.async_
    @pytest.mark.decoder
    def test_async_decode_file_pcm(self):
        assert LOOP.run_until_complete(async_decode_file(SILK_PATH))[:30] == EXPECT_DATA

    @pytest.mark.wav
    @pytest.mark.sync
    @pytest.mark.decoder
    def test_sync_decode_wav(self):
        wav = Wave_read(
            BytesIO(
                sync_decode(SILK_PATH, to_wav=True)
            )
        )
        assert wav.readframes(15) == EXPECT_DATA

    @pytest.mark.wav
    @pytest.mark.sync
    @pytest.mark.decoder
    def test_sync_decode_file_wav(self):
        wav = Wave_read(
            BytesIO(
                sync_decode_file(SILK_PATH, to_wav=True)
            )
        )
        assert wav.readframes(15) == EXPECT_DATA

    @pytest.mark.wav
    @pytest.mark.async_
    @pytest.mark.decoder
    def test_async_decode_wav(self):
        wav = Wave_read(
            BytesIO(
                LOOP.run_until_complete(
                    async_decode(SILK_PATH, to_wav=True)
                )
            )
        )
        assert wav.readframes(15) == EXPECT_DATA

    @pytest.mark.wav
    @pytest.mark.async_
    @pytest.mark.decoder
    def test_async_decode_file_wav(self):
        wav = Wave_read(
            BytesIO(
                LOOP.run_until_complete(
                    async_decode_file(SILK_PATH, to_wav=True)
                )
            )
        )
        assert wav.readframes(15) == EXPECT_DATA
