"""
Main entry point for the Legal Toolkit CLI.
"""

import argparse
import os
import sys
from .bundler import generate_bundle_index
from .deadlines import calculate_cpr_deadline

def main():
    parser = argparse.ArgumentParser(
        description="Legal Toolkit: Utilities for automated legal compliance and workflow."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: bundle
    parser_bundle = subparsers.add_parser("bundle", help="Generate court bundle index & check size compliance (CPR PD 5B)")
    parser_bundle.add_argument("--path", type=str, default=os.getcwd(), help="Directory path to bundle (default: current)")
    parser_bundle.add_argument("--court", type=str, choices=['general', 'county'], default='general', 
                               help="Target court for size limits (general=25MB, county=10MB)")

    # Subcommand: deadline
    parser_deadline = subparsers.add_parser("deadline", help="Calculate filing deadlines (CPR 10.3 & 2.8)")
    parser_deadline.add_argument("--date", type=str, required=True, help="Date of Service (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "bundle":
        generate_bundle_index(args.path, args.court)
    elif args.command == "deadline":
        calculate_cpr_deadline(args.date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
