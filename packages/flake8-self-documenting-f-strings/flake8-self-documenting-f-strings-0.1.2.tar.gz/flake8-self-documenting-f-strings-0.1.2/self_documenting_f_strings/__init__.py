"""Stop pycodestyle from calling valid self-documenting f-strings errors."""
import ast
import io
import re
import tokenize
from contextlib import redirect_stdout
from importlib.metadata import version
from typing import Any, Generator

import pycodestyle
from flake8.style_guide import Violation


class FStringChecker:
    """Allow valid self-documenting f-string code to be checked and not emmit false pycodestyle errors."""

    name = 'flake8-self-documenting-f-strings'
    version = version('flake8-self-documenting-f-strings')

    # These are the two incorrect errors that have been seen
    ignore_codes = {'E251', 'E202'}

    def __init__(self, tree: ast.Module, filename: str) -> None:
        """Initialize object."""
        self.tree = tree
        self.filename = filename
        self.fstrings = []
        with open(filename, 'r') as f:
            tokens = list(tokenize.generate_tokens(f.readline))
        for token in tokens:
            if token.type == tokenize.FSTRING_START:
                self.fstrings.append((token.start, token.end))

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Do the checking."""
        for error in self._get_ws_errors():
            if error.code not in self.ignore_codes or not self._in_fstring(error):
                yield (
                    error.line_number,
                    error.column_number,
                    error.text,
                    error.code,
                )

    def _in_fstring(self, error: Violation) -> bool:
        """Determine if the error is in an f-string or not."""
        line_number = error.line_number

        for start, end in self.fstrings:
            if start[0] <= line_number <= end[0]:
                return True

        return False

    def _get_ws_errors(self) -> list[Violation]:
        """Get all whitespace errors (E2) from pycodestyle.

        Format:
            List of (filename, line number, column, error code, message)
        """
        # Create a StringIO object to capture the output
        f = io.StringIO()

        # Create a pycodestyle.Checker
        checker = pycodestyle.Checker(self.filename)

        # Run pycodestyle and capture all of the errors with line numbers.
        # Their API doesn't seem to allow for this.
        with redirect_stdout(f):
            checker.check_all()

        # Parse out all of the errors
        errors = re.findall(r'(.*):(\d+):(\d+):\s+(E2\d+)\s+(.+)', f.getvalue())

        # Fix types and return Violations found
        return [Violation(e[3], e[0], int(e[1]), int(e[2]), e[4], None) for e in errors]
