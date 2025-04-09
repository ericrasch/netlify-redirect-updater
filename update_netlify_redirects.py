"""
################################################################################
# Script Name: update_netlify_redirects.py
#
# Description:
#   Updates a single Netlify `_redirects` file using a CSV map of `old_url,new_url`.
#   Only exact destination matches are replaced.
#
#   The script:
#     - Replaces URLs in `_redirects` if exact match found in CSV.
#     - Outputs `_redirects_updated` with pretty formatting (default).
#     - Generates an HTML diff report (`redirects_diff.html`) for QA.
#
# Author: Eric Rasch
# GitHub: https://github.com/ericrasch/netlify-redirect-updater
# Date Created: 2025-04-09
# Last Modified: 2025-04-09
# Version: 1.1
#
# Usage:
#   python update_netlify_redirects.py \
#     --csv redirects.csv \
#     --redirects _redirects \
#     --output _redirects_updated \
#     --diff redirects_diff.html
#
# Arguments:
#   --csv         CSV with header `old_url,new_url`
#   --redirects   Input `_redirects` file
#   --output      Path to write updated `_redirects` file
#   --diff        Path to write diff HTML file
#   --domain      (Optional) Limit updates to matching domains
#   --pretty      (Default) Align columns for readability
#   --no-pretty   Disable column alignment
################################################################################
"""

import argparse
import pandas as pd
from difflib import HtmlDiff

def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    return dict(zip(df.iloc[:, 0].str.strip(), df.iloc[:, 1].str.strip()))

def process_redirects(redirects_path, url_map, domain_filter):
    with open(redirects_path, "r") as f:
        lines = f.readlines()

    updated_lines = []
    replaced = 0
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1].startswith("https://"):
            target_url = parts[1].strip()
            if (not domain_filter or target_url.startswith(domain_filter)) and target_url in url_map:
                parts[1] = url_map[target_url]
                replaced += 1
            updated_line = "  ".join(parts)
        else:
            updated_line = line.strip()
        updated_lines.append(updated_line + "\n")
    return lines, updated_lines, replaced

def format_redirects(lines):
    redirects = []
    max_from = 0
    max_to = 0

    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3 and parts[1].startswith("https://"):
            from_url, to_url, status = parts
            redirects.append((from_url, to_url, status))
            max_from = max(max_from, len(from_url))
            max_to = max(max_to, len(to_url))
        else:
            redirects.append(line.strip())

    formatted = []
    for item in redirects:
        if isinstance(item, tuple):
            from_url, to_url, status = item
            formatted.append(f"{from_url.ljust(max_from + 2)}{to_url.ljust(max_to + 2)}{status}\n")
        else:
            formatted.append(item + "\n")
    return formatted

def write_diff(original, updated, diff_path):
    html_diff = HtmlDiff(wrapcolumn=100).make_file(original, updated, fromdesc="Original", todesc="Updated")
    with open(diff_path, "w") as f:
        f.write(html_diff)

def main():
    parser = argparse.ArgumentParser(description="Update Netlify _redirects file using a CSV map.")
    parser.add_argument("--csv", required=True, help="CSV file with old and new URLs")
    parser.add_argument("--redirects", required=True, help="Original Netlify _redirects file")
    parser.add_argument("--output", required=True, help="Path to write the updated _redirects file")
    parser.add_argument("--diff", required=True, help="Path to write the HTML diff")
    parser.add_argument("--domain", default="", help="Only replace URLs starting with this domain (optional)")
    parser.add_argument("--pretty", action="store_true", default=True, help="Enable column-aligned output formatting")
    parser.add_argument("--no-pretty", dest="pretty", action="store_false", help="Disable column-aligned output formatting")
    args = parser.parse_args()

    url_map = load_csv(args.csv)
    original_lines, updated_lines, replaced = process_redirects(args.redirects, url_map, args.domain)

    with open(args.output, "w") as f:
        f.writelines(format_redirects(updated_lines) if args.pretty else updated_lines)

    write_diff(original_lines, updated_lines, args.diff)

    print(f"✅ {replaced} replacements made.")
    print(f"📝 Updated file saved to {args.output}")
    print(f"📊 Diff file saved to {args.diff}")

if __name__ == "__main__":
    main()
