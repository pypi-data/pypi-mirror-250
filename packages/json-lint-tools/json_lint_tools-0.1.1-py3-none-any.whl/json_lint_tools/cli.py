from argparse import ArgumentParser
from glob import glob
from io import StringIO
from json import JSONDecodeError
from os import path
from sys import stdout, stdin
from typing import List

from . import Diff, TermColors


parser = ArgumentParser()

parser.add_argument(
    "path", help="Path to a single file or directory of JSON files", nargs="*"
)

parser.add_argument(
    "--check",
    help="Only check if the files would be changed. Show a list of any files that would be changed and exit with an error if any would be",
    action="store_true",
)

parser.add_argument("-d", "--diff", help="Show a diff", action="store_true")

parser.add_argument(
    "-f", "--format", action="store_true", help="Format non-conforming files"
)

parser.add_argument(
    "-i",
    "--indent",
    type=int,
    help="How many spaces are expected per indentation",
    default=2,
)

parser.add_argument(
    "--no-color", help="Don't print colors to stdout", action="store_true"
)

parser.add_argument(
    "-r", "--recursive", action="store_true", help="Search recursively for JSON files"
)

parser.add_argument(
    "-s",
    "--sort",
    dest="sort_all",
    action="store_true",
    help="Sort all objects by key and all arrays alphabetically. Shorthand for --sort-keys + --sort-arrays",
)

parser.add_argument(
    "--sort-arrays", action="store_true", help="Sort arrays alphabetically"
)

parser.add_argument(
    "--sort-keys", action="store_true", help="Sort keys in JSON objects alphabetically"
)

parser.add_argument(
    "--stdin", help="Read data from stdin instead of a file", action="store_true"
)

args = parser.parse_args()


def exit_error(msg: str | List[str], code: int = 1, prefix=True) -> None:
    if prefix:
        name = f"{__name__.split('.')[0]}: "
    else:
        name = ""
    if isinstance(msg, str):
        msg = name + msg
        print(msg)
    else:
        if name:
            msg = [f"{name}\n"] + msg
        stdout.writelines(msg)
    exit(code)


def parse_paths(paths: List[str], recursive: bool = True):
    files = []

    for fpath in paths:
        if path.isdir(fpath):
            if recursive:
                fpath = f"{fpath}/**/*.json"
            else:
                fpath = f"{fpath}/*.json"
            files += glob(fpath, recursive=recursive)
        elif not path.isfile(fpath):
            exit_error(f"{fpath}: No such file or directory")
        else:
            files.append(fpath)

    return files


def print_offenders(fnames: List[str]):
    color = TermColors.RED if not args.no_color else ""
    end = TermColors.END if not args.no_color else ""
    fails = [f"  {color}{fname}{end}\n" for fname in fnames]
    out = ["The following files would be formatted:\n"] + fails
    exit_error(out, 1, prefix=False)


def check_args():
    code = 0
    if args.check and any((args.diff, args.format)):
        msg = "Args --check cannot be used with --diff or --fmt\n"
        code = 2

    if stdin.isatty() and not args.path:
        msg = "jsonlint: error: the following arguments are required: path"
        code = 2

    if args.sort_all:
        args.sort_arrays = True
        args.sort_keys = True

    if code:
        parser.print_help()
        msg = f"{TermColors.RED}{msg}{TermColors.END}"
        print(msg)
        exit(code)


def run():
    check_args()
    fails = []
    is_stdin = args.stdin or not stdin.isatty()
    color = not args.no_color

    if is_stdin:
        fobj = StringIO()
        fobj.write(stdin.read())
        fobj.seek(0)
        files = [fobj]
    else:
        files = parse_paths(args.path, recursive=args.recursive)

    for fpath in files:
        opts = dict(
            indent=args.indent,
            sort_arrays=args.sort_arrays or args.sort_all,
            sort_keys=args.sort_keys or args.sort_all,
        )
        if isinstance(fpath, str):
            opts["filepath"] = fpath
        else:
            opts["fileobj"] = fpath

        try:
            diff = Diff(**opts)
        except JSONDecodeError as e:
            exit_error(f"JSON Error: {e}", 1)

        if is_stdin:
            if args.diff:
                diff.print_diff(color=color)
                print("")
            else:
                diff.format_file()

            if diff.is_diff:
                exit(1)

        if diff.is_diff and not is_stdin:
            fails.append(fpath)

        if args.format and diff.is_diff:
            diff.format_file()
            continue

        if args.check:
            if diff.is_diff:
                exit(1)

        if args.diff:
            diff.print_diff(color=color)
            print("")

    if fails and not args.diff and not args.format:
        print_offenders(fails)


def main():
    try:
        run()
    except KeyboardInterrupt:
        exit(130)
    except Exception as e:
        exit_error(e, 255)
