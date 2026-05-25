import argparse
import json
import sys

from rich.console import Console

from .core import analyse_file

console = Console()


def main():
    from lens_contract import run_contract_subcommands

    from .manifest import MANIFEST

    # `serve` and `manifest` are the family's shared subcommands (lens-contract).
    if run_contract_subcommands(
        MANIFEST,
        app_path="wordpress_analyser.api:app",
        default_port=8005,
        env_prefix="WORDPRESS_ANALYSER",
    ):
        return

    parser = argparse.ArgumentParser(
        prog="wordpress-analyser",
        description="Analyse a WordPress PHP file for hooks, API usage, and quality signals",
        epilog="subcommands: `serve` (run the HTTP API), `manifest` (print the capability manifest)",
    )
    parser.add_argument("file", help="Path to a .php file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

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
