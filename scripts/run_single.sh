#!/bin/bash

# Single-site redirect update
# Update the values below to match your file names

CSV="redirects.csv"
REDIRECTS="_redirects"
OUTPUT="_redirects_updated"
DIFF="redirects_diff.html"
DOMAIN="https://your-domain.com"

python3 update_netlify_redirects.py \
  --csv "$CSV" \
  --redirects "$REDIRECTS" \
  --output "$OUTPUT" \
  --diff "$DIFF" \
  --domain "$DOMAIN"
