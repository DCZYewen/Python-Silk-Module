import argparse

from . import encode_file, decode_file
from .utils import get_file
from .wav import Wave

parser = argparse.ArgumentParser("pysilk", description="encode/decode your silk file")
parser.add_argument("-r", "--rate", default=24000, help="set pcm framerate")
parser.add_argument("input", action="store")
parser.add_argument("output", action="store")


def get_suffix(path: str):
    sp = path.rsplit(".", 1)
    if len(sp) == 1:
        raise ValueError("cannot parse suffix")
    elif sp[1] not in ("wav", "pcm", "silk"):
        raise TypeError("%s format not supported" % sp[1])
    else:
        return sp[1]


if __name__ == '__main__':
    args = parser.parse_args()
    if get_suffix(args.input) == get_suffix(args.output):
        print("nothing can do.")
    elif get_suffix(args.input) == "pcm" and not args.rate:
        raise ValueError("--rate must be set")
    else:
        with open(args.output, "wb") as f:
            source = args.input
            if get_suffix(args.input) == "wav" and get_suffix(args.output) == "pcm":
                f.write(Wave.wav2pcm(get_file(source)))
            elif get_suffix(args.input) == "pcm" and get_suffix(args.output) == "wav":
                f.write(Wave.pcm2wav(get_file(source), args.rate))
            elif get_suffix(args.input) in ("pcm", "wav") and get_suffix(args.output) == "silk":
                f.write(encode_file(source))
            elif get_suffix(args.input) == "silk" and get_suffix(args.output) in ("pcm", "wav"):
                f.write(decode_file(source, to_wav=args.output == "wav"))
            else:
                print("Unknown operation:", get_suffix(args.input), "to", get_suffix(args.output))
    print(args)
