import argparse
import sys
from pathlib import Path

from . import decode, encode, install


def main():
    parser = argparse.ArgumentParser(prog="ipy")
    commands = parser.add_subparsers(dest="command", required=True)
    encoder = commands.add_parser("encode", help="Encode a Python source file")
    encoder.add_argument("file")
    encoder.add_argument("-o", "--output")
    runner = commands.add_parser("run", help="Run an invisible Python file")
    runner.add_argument("file")
    runner.add_argument("args", nargs=argparse.REMAINDER)
    cat = commands.add_parser("cat", help="Write decoded source to stdout")
    cat.add_argument("file")
    args = parser.parse_args()
    filename = Path(args.file)

    if args.command == "encode":
        output = Path(args.output) if args.output else filename.with_suffix(".ipy")
        output.write_bytes(encode(filename.read_bytes()))
    elif args.command == "cat":
        sys.stdout.buffer.write(decode(filename.read_bytes()))
    else:
        source = decode(filename.read_bytes())
        sys.argv = [args.file, *args.args]
        sys.path.insert(0, str(filename.resolve().parent))
        install()
        exec(compile(source, args.file, "exec"), {
            "__name__": "__main__",
            "__file__": args.file,
            "__package__": None,
        })


if __name__ == "__main__":
    main()
