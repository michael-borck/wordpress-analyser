from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wordpress-analyser",
        description="WordPress theme and plugin analyser (coming soon)",
    )
    parser.add_argument("path", nargs="?", help="WordPress theme or plugin directory")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--version", action="version", version="0.1.0")

    subparsers = parser.add_subparsers(dest="command")
    serve = subparsers.add_parser("serve", help="Start API server")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8005)

    args = parser.parse_args()

    if args.command == "serve":
        print("wordpress-analyser serve — not yet implemented", file=sys.stderr)
        sys.exit(1)

    if not args.path:
        parser.print_help()
        sys.exit(1)

    print("wordpress-analyser — not yet implemented", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
