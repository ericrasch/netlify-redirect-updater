"""
################################################################################
# Script Name: update_netlify_redirects.py
#
# Description:
#   CLI tool to update a single Netlify `_redirects` file using a CSV mapping
#   of `old_url,new_url` pairs. Only exact matches are updated to ensure
#   precision and control over redirect behaviors.
#
#   Generates an updated `_redirects` file and an HTML diff report to visually
#   audit the changes made.
#
# Author: Eric Rasch
# GitHub: https://github.com/ericrasch/netlify-redirect-updater
# Date Created: 2025-04-09
# Last Modified: 2025-04-09
# Version: 1.0
#
# Usage:
#   python update_netlify_redirects.py \\
#     --csv redirects.csv \\
#     --redirects _redirects \\
#     --output _redirects_updated \\
#     --diff redirects_diff.html \\
#     --domain https://your-domain.com
#
# Arguments:
#   --csv         CSV file with `old_url,new_url` columns
#   --redirects   Path to original Netlify `_redirects` file
#   --output      Output path for the updated `_redirects` file
#   --diff        Path to write the HTML diff report
#   --domain      (Optional) Only update URLs that start with this domain
#
# Output:
#   - Updated `_redirects` file with modified destination URLs
#   - HTML diff report comparing original and updated files
#
# Notes:
#   - Lines not matching the CSV are preserved exactly as-is
#   - Only URLs beginning with `https://` are considered for replacement
#   - Requires Python 3.7+ and the `pandas` library
################################################################################
"""

import argparse
import pandas as pd
from difflib import HtmlDiff, unified_diff

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
            target_url = parts[1]
            if (not domain_filter or target_url.startswith(domain_filter)) and target_url in url_map:
                parts[1] = url_map[target_url]
                replaced += 1
            updated_line = "  ".join(parts)
        else:
            updated_line = line.strip()
        updated_lines.append(updated_line + "\n")
    return lines, updated_lines, replaced

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

    args = parser.parse_args()

    url_map = load_csv(args.csv)
    original_lines, updated_lines, replaced = process_redirects(args.redirects, url_map, args.domain)

    with open(args.output, "w") as f:
        f.writelines(updated_lines)

    write_diff(original_lines, updated_lines, args.diff)

    print(f"✅ {replaced} replacements made.")
    print(f"📝 Updated file saved to: {args.output}")
    print(f"📊 Diff file saved to: {args.diff}")

if __name__ == "__main__":
    main()
