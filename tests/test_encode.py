import pytest
from utils import local_file, get_loop

PCM_PATH = local_file("target.pcm")
WAV_PATH = local_file("target.wav")
LOOP = get_loop()


def sync_encode(path: str):
    from pysilk import encode
    from pysilk.utils import is_silk_data

    with open(path, "rb") as f:
        assert is_silk_data(encode(f.read()))


def sync_encode_file(path: str):
    from pysilk import encode_file
    from pysilk.utils import is_silk_data

    assert is_silk_data(encode_file(path))


async def async_encode(path: str):
    from pysilk import async_encode
    from pysilk.utils import is_silk_data

    with open(path, "rb") as f:
        data = await async_encode(f.read())
        print(data)
        assert is_silk_data(data)


async def async_encode_file(path: str):
    from pysilk import async_encode_file
    from pysilk.utils import is_silk_data

    assert is_silk_data(await async_encode_file(path))


class TestEncode:
    @pytest.mark.pcm
    @pytest.mark.sync
    @pytest.mark.encoder
    def test_sync_encode_pcm(self):
        sync_encode(PCM_PATH)

    @pytest.mark.pcm
    @pytest.mark.sync
    @pytest.mark.encoder
    def test_sync_encode_file_pcm(self):
        sync_encode_file(PCM_PATH)

    @pytest.mark.wav
    @pytest.mark.sync
    @pytest.mark.encoder
    def test_sync_encode_wav(self):
        sync_encode(WAV_PATH)

    @pytest.mark.wav
    @pytest.mark.sync
    @pytest.mark.encoder
    def test_sync_encode_file_wav(self):
        sync_encode_file(WAV_PATH)

    @pytest.mark.pcm
    @pytest.mark.async_
    @pytest.mark.encoder
    def test_async_encode_pcm(self):
        LOOP.run_until_complete(async_encode(PCM_PATH))

    @pytest.mark.pcm
    @pytest.mark.async_
    @pytest.mark.encoder
    def test_async_encode_file_pcm(self):
        LOOP.run_until_complete(async_encode_file(PCM_PATH))

    @pytest.mark.wav
    @pytest.mark.async_
    @pytest.mark.encoder
    def test_async_encode_wav(self):
        LOOP.run_until_complete(async_encode(WAV_PATH))

    @pytest.mark.wav
    @pytest.mark.async_
    @pytest.mark.encoder
    def test_async_encode_file_wav(self):
        LOOP.run_until_complete(async_encode_file(WAV_PATH))
