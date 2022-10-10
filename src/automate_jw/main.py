# Script entrypoints

from argparse import ArgumentParser

from automate_jw.process_url import NoMatchingRule, process_url


def get_process_url_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Process a URL for an OmniFocus task.")
    parser.add_argument("url", help="URL to add as OmniFocus task")
    return parser


def process_url_main() -> int:
    parser = get_process_url_parser()
    args = parser.parse_args()
    try:
        commands = process_url(url=args.url)
    except NoMatchingRule:
        return 1
    print("\n".join(commands))
    return 0
