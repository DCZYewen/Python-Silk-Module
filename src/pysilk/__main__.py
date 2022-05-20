import argparse
import time

from . import encode_file, decode_file
from .utils import get_file, play_audio
from .wav import Wave

parser = argparse.ArgumentParser("pysilk", description="encode/decode your silk file")
parser.add_argument("-r", "--rate", default=24000, type=int, help="set silk output datarate")
parser.add_argument("-p", "--play", action="store_true", help="play input file")
parser.add_argument("-q", "--quiet", action="store_true", help="reduce console output")
parser.add_argument("--sample-rate", default=24000, type=int, help="set pcm output samplerate")
parser.add_argument("input", action="store", type=str, help="input file path")
parser.add_argument("output", help="output file path", nargs="?", default="")


def get_suffix(path: str) -> str:
    if path:
        sp = path.rsplit(".", 1)
        if len(sp) == 1:
            raise ValueError("cannot parse suffix")
        elif sp[1] not in ("wav", "pcm", "silk"):
            raise TypeError("%s format not supported" % sp[1])
        else:
            return sp[1]


def log(*content_args):
    if not args.quiet:
        print(*content_args)


if __name__ == '__main__':
    st = time.time()
    args = parser.parse_args()
    i_suffix, o_suffix = get_suffix(args.input), get_suffix(args.output)
    if args.play:
        log("playing:", args.input)
        if i_suffix == "wav":
            play_audio(args.input)
        elif i_suffix == "pcm":
            play_audio(Wave.pcm2wav(get_file(args.input), args.sample_rate))
        elif i_suffix == "silk":
            play_audio(decode_file(args.input, to_wav=True))
    elif i_suffix == o_suffix or not o_suffix:
        log("nothing can do.")
    elif i_suffix == "pcm" and not args.sample_rate:
        raise ValueError("--sample-rate must be set")
    else:
        with open(args.output, "wb") as f:
            source = args.input
            if i_suffix == "wav" and o_suffix == "pcm":
                f.write(Wave.wav2pcm(get_file(source)))
            elif i_suffix == "pcm" and o_suffix == "wav":
                f.write(Wave.pcm2wav(get_file(source), args.sample_rate))
            elif i_suffix in ("pcm", "wav") and o_suffix == "silk":
                f.write(encode_file(source, args.rate))
            elif i_suffix == "silk" and o_suffix in ("pcm", "wav"):
                f.write(decode_file(source, to_wav=args.output == "wav"))
            else:
                print("Unknown operation:", i_suffix, "to", o_suffix)
    log(f"done, {round((time.time() - st) * 1000, 2)}ms used")
