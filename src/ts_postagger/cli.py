"""Command-line interface for ts-postagger."""

import argparse
from importlib.metadata import PackageNotFoundError, version
import sys

from .api import pos


def _get_version() -> str:
    try:
        return version("ts-postagger")
    except PackageNotFoundError:
        return "0+local"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ts-postagger",
        description="Turkish POS tagging from text or stdin.",
        epilog=(
            "Examples:\n"
            "  ts-postagger \"Bugün yeni ve güzel bir gün!\"\n"
            "  ts-postagger -low \"Bugün yeni ve güzel bir gün!\"\n"
            "  ts-postagger -tag \"Bugün yeni ve güzel bir gün!\"\n"
            "  ts-postagger --full \"Bugün yeni ve güzel bir gün!\"\n"
            "  echo \"Bugün yeni ve güzel bir gün!\" | ts-postagger"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    parser.add_argument("text", nargs="?", help="Text to analyze. Reads stdin when omitted.")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {_get_version()}",
        help="Show version and exit.",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-low",
        action="store_true",
        help="Print lowercase forms only.",
    )
    output_group.add_argument(
        "-tag",
        action="store_true",
        help="Print token and raw model tag.",
    )
    output_group.add_argument(
        "--full",
        action="store_true",
        help="Print token, lower, and final pos.",
    )
    return parser


def _format_token(token, args: argparse.Namespace) -> str:
    if args.low:
        return token.lower
    if args.tag:
        return f"{token.text}\t{token.tag}"
    if args.full:
        return f"{token.text}\t{token.lower}\t{token.pos}"
    return f"{token.text}\t{token.pos}"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    tokens = pos(text)

    for token in tokens:
        sys.stdout.write(_format_token(token, args))
        sys.stdout.write("\n")

    return 0
