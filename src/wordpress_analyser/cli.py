import argparse
import json
import sys
import uvicorn
from pathlib import Path

from rich.console import Console

from .core import analyse_file

console = Console()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordpress-analyser",
        description="Analyse a WordPress PHP file for hooks, API usage, and quality signals",
    )
    sub = parser.add_subparsers(dest="command")

    # serve subcommand
    serve = sub.add_parser("serve", help="Start the HTTP API server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8005)

    # manifest subcommand
    sub.add_parser("manifest", help="Print the capability manifest as JSON")

    # analyse subcommand (also the default when no subcommand is given)
    analyse = sub.add_parser("analyse", help="Analyse a WordPress PHP file (default)")
    analyse.add_argument("file", help="Path to a .php file")
    analyse.add_argument("--json", action="store_true", help="Output as JSON")

    return parser


def main():
    # Support the short form: wordpress-analyser <file> [--json]
    # by detecting whether the first non-flag arg looks like a subcommand.
    argv = sys.argv[1:]

    if argv and not argv[0].startswith("-") and argv[0] not in {"serve", "analyse", "manifest"}:
        argv = ["analyse"] + argv

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "manifest":
        from .manifest import MANIFEST
        print(json.dumps(MANIFEST, indent=2))
        return

    if args.command == "serve":
        uvicorn.run("wordpress_analyser.api:app", host=args.host, port=args.port)
        return

    if args.command == "analyse":
        result = analyse_file(args.file)

        if args.json:
            print(json.dumps(result.model_dump(), indent=2))
            return

        if result.error:
            console.print(f"[red]Error:[/red] {result.error}")
            sys.exit(1)

        # Rich output
        console.print(f"\n[bold]WordPress Analysis:[/bold] {result.filename}")
        console.print(
            f"Type: {result.detected_type}  |  Lines: {result.line_count}"
            f"  |  Functions: {result.function_count}  |  Classes: {result.class_count}"
        )
        console.print(f"Hooks: {result.action_count} actions, {result.filter_count} filters")
        if result.shortcodes:
            console.print(f"Shortcodes: {', '.join(result.shortcodes)}")
        if result.post_types:
            console.print(f"Post types: {', '.join(result.post_types)}")
        if result.direct_db_queries:
            console.print(f"[yellow]Direct DB queries:[/yellow] {result.direct_db_queries}")
        if result.nonce_checks:
            console.print(f"Nonce checks: {result.nonce_checks}")
        return

    # No command given — print help
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
