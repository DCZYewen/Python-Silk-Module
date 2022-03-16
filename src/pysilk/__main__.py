import argparse
import time

from . import encode_file, decode_file
from .utils import get_file
from .wav import Wave

parser = argparse.ArgumentParser("pysilk", description="encode/decode your silk file")
parser.add_argument("-sr", "--sample-rate", default=24000, help="set pcm samplerate")
parser.add_argument("-q", "--quiet", action="store_const", const=bool, default=False, help="reduce console output")
parser.add_argument("input", action="store", help="input file path")
parser.add_argument("output", action="store", help="output file path")


def get_suffix(path: str):
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
    if i_suffix == o_suffix:
        print("nothing can do.")
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
                f.write(encode_file(source))
            elif i_suffix == "silk" and o_suffix in ("pcm", "wav"):
                f.write(decode_file(source, to_wav=args.output == "wav"))
            else:
                print("Unknown operation:", i_suffix, "to", o_suffix)
    log(f"done, {round(time.time() - st, 2)}ms used")
