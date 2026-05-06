import argparse
import json
import sys
import uvicorn
from pathlib import Path

from rich.console import Console

from .core import analyse_file

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="wordpress-analyser",
        description="Analyse a WordPress PHP file for hooks, API usage, and quality signals",
    )
    sub = parser.add_subparsers(dest="command")
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true")
    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8005)

    args = parser.parse_args()

    if args.command == "serve":
        uvicorn.run("wordpress_analyser.api:app", host=args.host, port=args.port)
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

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


if __name__ == "__main__":
    main()
