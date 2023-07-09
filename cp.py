import sys
import argparse

from logger import logger
from db.setup import initial_db_setup
from db.controller import add_setting

from cfformat.cfformatter import CustomArgvParser, ArgvFormatter
from fshelper.fshelper import write_to_file
from cfparser.cfparser import parse_contest

parser = CustomArgvParser(
    description = 'Process contest ID',
    formatter_class = ArgvFormatter,
)

parser.add_argument(
    '-c',
    '--contestId',
    type = int,
    help = 'Codeforces contest ID, that shows after the URL.'
)

parser.add_argument(
    '-s',
    '--setting',
    nargs=2,
    help='User setting name'
)

parser.add_argument(
    '-v',
    '--verbose',
    action=argparse.BooleanOptionalAction,
    help='User setting name'
)

args = parser.parse_args()

def handle_setting_argv():
    """
        Handle settings related argv
    """
    if args.setting:
        add_setting(args.setting[0], args.setting[1])
        print(f"Setting {args.setting[0]} has been set to {args.setting[1]}.")
        sys.exit(0)

def handle_verbose_argv():
    """
        Handle the -v / --verbose option
    """
    if args.verbose:
        logger.set_log_level(logger.LogLevel.INFO)

def handle_contest_id_argv():
    """
        Handle contest ID argv
    """
    if not args.contestId:
        logger.fetal("Contest ID is required! Hint: <script.py> -c <contestId>")

def main():
    """main function"""

    # handle command line arguments
    handle_verbose_argv()
    handle_setting_argv()
    handle_contest_id_argv()


    # db setup
    # needs to be done before main application runs.
    # can cause issue in new application if not called
    initial_db_setup()

    logger.success("Welcome")
    logger.info('Info log')
    logger.error('error')
    parse_contest(contest_id=args.contestId)


# executes the main function if called as a script
if __name__ == '__main__':
    main()
