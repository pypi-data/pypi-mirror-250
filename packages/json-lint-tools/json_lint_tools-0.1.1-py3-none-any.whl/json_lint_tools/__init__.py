#!/usr/bin/env python3
from difflib import unified_diff
from io import StringIO
from json import load, dumps
from os import path
from sys import stdout
from typing import IO, Dict, List


class TermColors:
    """
    Simple way of referencing ANSI color escapes for terminal output
    """

    #: End ANSI colors
    END = "\033[0m"
    #: ANSI Green
    GREEN = "\033[92m"
    #: ANSI Red
    RED = "\033[91m"
    #: ANSI White
    WHITE = "\033[97m"


class Diff:
    """
    Creates an object that can compares a JSON string to what would be created using `json.dumps` and provides tools for using as a cli tool.

    :param filepath: Optional relative or absolute path to a file to work with. You must provide one of `filepath` or `fileobj`.
    :param fileobj: Optional file or file-like object, such as the return of `open()` or a `StringIO` object. Must implement `read`, `readlines`, and `seek`. You must provide one of `filepath` or `fileobj`.
    :param indent: Number of indentions to check against
    :param sort_arrays: If `True` values in all arrays in the JSON will be sorted alphabetically.
    :param sort_keys: If `True` keys in all objects in the JSON will be sorted alphabetically

    """

    def __init__(
        self,
        filepath: str = "",
        fileobj: IO = None,
        indent: int = 2,
        sort_arrays: bool = False,
        sort_keys: bool = False,
    ):
        self.__original_lines: List[str] = None
        self.__formatted_lines: List[str] = None
        self.__diff_output: List[str] = None

        #: The input JSON after being formatted
        self.formatted_data: str = None

        self.sort_arrays: bool = sort_arrays
        self.sort_keys: bool = sort_keys
        self.indent: int = indent
        self.filepath: str = filepath
        self.fileobj: IO = fileobj

        #: Absolute path to file. Will be an empty string with using `fileobj`
        self.abspath: str = path.abspath(filepath) if filepath else ""

        if not (filepath or fileobj):
            raise AttributeError("You must pass one of `path` or `fileobj`")

        if self.filepath:
            self.__load_from_filepath()
        else:
            self.__load_from_io()

        # This handles strange behaviour in diff output when the source is a single line
        # and doesn't contain a newline ending
        if len(self.__original_lines) == 1 and not self.__original_lines[0].endswith(
            "\n"
        ):
            self.__original_lines[0] += "\n"

        # Create a file like object and write the formatted data to it. This allows us to treat
        # files on disk and the formatted data in the same way
        tmp = StringIO()
        tmp.write(self.formatted_data)
        tmp.seek(0)
        self.__formatted_lines = tmp.readlines()

    def format_file(self) -> None:
        """
        Will write the formatted JSON back to the original file if working with a file path.
        When working with a file or file-like object the formatted JSON will be printed to stdout
        """
        if self.fileobj:
            self.print()
            return

        with open(self.filepath, "w") as f:
            f.write(self.formatted_data)

    def get_diff(self) -> List[str]:
        """
        Return a diff to be used as visual output as an list of strings using the `difftools.unified_diff` packagge
        """
        if self.__diff_output is not None:
            return self.__diff_output

        self.__diff_output = list(
            unified_diff(self.__original_lines, self.__formatted_lines)
        )

        return self.__diff_output

    @property
    def is_diff(self) -> bool:
        """
        Check if the input would be changed at all
        """
        return self.__formatted_lines != self.__original_lines

    def print(self) -> None:
        """
        Print the pretty formatted JSON to stdout
        """
        print(self.formatted_data)

    def print_diff(self, color: bool = True) -> None:
        """
        Prints the diff output to stdout, optionally using term colors

        :param color: Optionally print with color. Red for deletions and green for additions
        """
        out = [f"File: {self.filepath}\n"]

        if color:
            for line in self.get_diff():
                if line.startswith("-"):
                    color = TermColors.RED
                elif line.startswith("+"):
                    color = TermColors.GREEN
                else:
                    color = TermColors.WHITE

                out.append(f"{color}{line}{TermColors.END}")
        else:
            out = out + self.get_diff()

        stdout.writelines(out)

    def __load_from_filepath(self) -> None:
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.__original_lines = f.readlines()
            f.seek(0)

            data = load(f)

            if self.sort_arrays:
                data = self.__sort_arrays(data)

            self.formatted_data = dumps(
                data, indent=self.indent, sort_keys=self.sort_keys
            )

    def __load_from_io(self) -> None:
        self.__original_lines = self.fileobj.readlines()

        self.fileobj.seek(0)
        data = load(self.fileobj)

        if self.sort_arrays:
            data = self.__sort_arrays(data)

        formatted_data = dumps(data, indent=self.indent, sort_keys=self.sort_keys)

        return formatted_data

    def __sort_arrays(self, data: Dict | List) -> Dict | List:
        if isinstance(data, list):
            data = enumerate(data)
        elif isinstance(data, dict):
            data = data.items()
        else:
            return data

        for k, v in data:
            if isinstance(v, list):
                data[k] = sorted(v)
            if isinstance(v, dict):
                data[k] = self.__sort_arrays(v)

        return data
