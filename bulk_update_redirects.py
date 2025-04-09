"""
################################################################################
# Script Name: bulk_update_redirects.py
#
# Description:
#   Scans a top-level directory where each subfolder contains:
#     - `_redirects`: The original Netlify redirect file
#     - `redirects.csv`: A CSV file with `old_url,new_url` mappings
#
#   For each project folder, this script:
#     - Replaces matching destination URLs using exact matches from the CSV
#     - Outputs an updated `_redirects_updated` file
#     - Generates an HTML diff report (`redirects_diff.html`) for QA
#     - Logs errors and prints a summary per folder
#
# Author: Eric Rasch
# GitHub: https://github.com/ericrasch/netlify-redirect-updater
# Date Created: 2025-04-09
# Last Modified: 2025-04-09
# Version: 1.1
#
# Usage:
#   python bulk_update_redirects.py \
#     --projects-folder /path/to/projects \
#     --domain https://your-domain.com
#
# Arguments:
#   --projects-folder   Path to top-level directory containing subfolders
#   --domain            (Optional) Restrict updates to URLs under this domain
#   --pretty            (Default) Align columns for readability
#   --no-pretty         Disable column alignment
#
# Output:
#   - _redirects_updated         (in each folder)
#   - redirects_diff.html        (in each folder)
#   - Error summary printed to console if issues occur
#
# Folder Structure:
#   /projects/
#     /site-a/
#       _redirects
#       redirects.csv
#     /site-b/
#       _redirects
#       redirects.csv
#
# Notes:
#   - `redirects.csv` must have a header row with `old_url,new_url`
#   - Only exact destination matches will be replaced
################################################################################
"""

import argparse
import os
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

def process_folder(folder_path, domain_filter, pretty, errors):
    csv_path = os.path.join(folder_path, "redirects.csv")
    redirects_path = os.path.join(folder_path, "_redirects")
    output_path = os.path.join(folder_path, "_redirects_updated")
    diff_path = os.path.join(folder_path, "redirects_diff.html")

    try:
        if not os.path.isfile(csv_path):
            raise FileNotFoundError("Missing redirects.csv")
        if not os.path.isfile(redirects_path):
            raise FileNotFoundError("Missing _redirects")

        url_map = load_csv(csv_path)
        original_lines, updated_lines, replaced = process_redirects(redirects_path, url_map, domain_filter)

        with open(output_path, "w") as f:
            f.writelines(format_redirects(updated_lines) if pretty else updated_lines)
        write_diff(original_lines, updated_lines, diff_path)

        print(f"✅ {folder_path}: {replaced} replacements made.")
        print(f"📝 Updated file saved to {output_path}")
        print(f"📊 Diff file saved to {diff_path}")
        print("")
        return True
    except Exception as e:
        error_msg = f"❌ {folder_path}: {str(e)}"
        print(error_msg)
        errors.append(error_msg)
        return False

def main():
    parser = argparse.ArgumentParser(description="Bulk update Netlify _redirects files in folder structure.")
    parser.add_argument("--projects-folder", required=True, help="Top-level folder containing project subfolders")
    parser.add_argument("--domain", default="", help="Only replace URLs starting with this domain (optional)")
    parser.add_argument("--pretty", action="store_true", default=True, help="Enable column-aligned output formatting")
    parser.add_argument("--no-pretty", dest="pretty", action="store_false", help="Disable column-aligned output formatting")
    args = parser.parse_args()

    errors = []
    for name in sorted(os.listdir(args.projects_folder)):
        subfolder = os.path.join(args.projects_folder, name)
        if os.path.isdir(subfolder):
            process_folder(subfolder, args.domain, args.pretty, errors)

    if errors:
        print("\n--- Error Summary ---")
        for err in errors:
            print(err)

if __name__ == "__main__":
    main()
