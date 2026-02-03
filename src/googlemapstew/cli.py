"""Command-line interface for googlemapstew."""

import argparse
import json
import sys
from pathlib import Path

from googlemapstew import GoogleMapsScraper


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract information from Google Maps HTML files"
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the HTML file to parse"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output as JSON (default format)"
    )
    parser.add_argument(
        "-p", "--pretty",
        action="store_true",
        help="Pretty print JSON output"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s 0.1.0"
    )

    args = parser.parse_args()

    # Check if file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    # Parse the HTML file
    scraper = GoogleMapsScraper()
    try:
        result = scraper.parse_file(str(file_path))
    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        return 1

    # Format output
    output = json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"Output written to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())