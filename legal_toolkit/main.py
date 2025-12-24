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
    parser_deadline = subparsers.add_parser("deadline", help="Calculate filing deadlines (CPR 6.14, 6.26, 10.3 & 2.8)")
    parser_deadline.add_argument("--date", type=str, required=True, help="Date of Transmission (e.g., 'YYYY-MM-DD', 'tomorrow', 'Friday', '25 Dec 2024')")
    parser_deadline.add_argument("--time", type=str, default="12:00", help="Time of Transmission (HH:MM, default 12:00)")
    parser_deadline.add_argument("--jurisdiction", type=str, choices=['england-and-wales', 'scotland', 'northern-ireland'], 
                                 default='england-and-wales', help="Jurisdiction for bank holidays")

    args = parser.parse_args()

    if args.command == "bundle":
        generate_bundle_index(args.path, args.court)
    elif args.command == "deadline":
        # Capture the returned dictionary
        result = calculate_cpr_deadline(args.date, args.time, args.jurisdiction)
        
        # Check for errors in the logic
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        else:
            # Print a clean summary using the data we got back
            print("\n" + "="*40)
            print(f"⚖️  CPR DEADLINE CALCULATOR")
            print("="*40)
            print(f"📅 Date Sent:       {result['sent_at']}")
            print(f"🚀 Deemed Service:  {result['deemed_service']}")
            print(f"🛑 Filing Deadline: {result['filing_deadline']}")
            print("="*40 + "\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
