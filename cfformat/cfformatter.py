"""
    This module contains all the formatter needed for this application.
    @author: Ashikur Rahman
"""

import sys as _sys
from collections.abc import Iterable
from typing import NoReturn
from argparse import _MutuallyExclusiveGroup, Action, ArgumentDefaultsHelpFormatter, ArgumentParser

from colorer.colorer import colored_text

class ArgvFormatter(ArgumentDefaultsHelpFormatter):
    """
        Argument formatter for parsing arguments
    """
    def add_usage(
            self, usage: str | None,
            actions: Iterable[Action],
            groups: Iterable[_MutuallyExclusiveGroup],
            prefix: str | None = None
        ) -> None:

        colored_usage_prefix = colored_text('USAGE: ', 'cyan')

        return super().add_usage(usage, actions, groups, prefix=colored_usage_prefix)

class CustomArgvParser(ArgumentParser):
    "Custom parser"
    def error(self, message: str) -> NoReturn:
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        colored_error_prefix = colored_text('ERROR: ', 'red', attrs=['bold'])
        self.print_usage(_sys.stderr)
        self.exit(2, f'{colored_error_prefix}{self.prog}: {message}\n')
