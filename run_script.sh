#!/bin/bash

echo "=========================================="
echo " Netlify Redirect Updater"
echo "=========================================="
echo "Choose mode:"
echo "1) Single-site update"
echo "2) Bulk project update"
read -p "Enter 1 or 2: " MODE

if [ "$MODE" != "1" ] && [ "$MODE" != "2" ]; then
  echo "❌ Invalid choice. Exiting."
  exit 1
fi

echo ""
echo "✅ Requirements Checklist:"
if [ "$MODE" == "1" ]; then
  echo "- redirects.csv file in the current folder"
  echo "- _redirects file in the current folder"
  echo "- CSV must have a header row: old_url,new_url"

  [ -f "redirects.csv" ] || { echo "❌ Missing redirects.csv"; exit 1; }
  [ -f "_redirects" ] || { echo "❌ Missing _redirects"; exit 1; }

else
  echo "- /projects/ folder in the current directory"
  echo "- Each subfolder must contain:"
  echo "    - _redirects"
  echo "    - redirects.csv"
  echo "- CSVs must have a header row: old_url,new_url"

  if [ ! -d "projects" ]; then
    echo "❌ Missing projects/ directory"
    exit 1
  fi

  errors=0
  for folder in projects/*; do
    [ -d "$folder" ] || continue
    if [ ! -f "$folder/redirects.csv" ] || [ ! -f "$folder/_redirects" ]; then
      echo "❌ Missing required files in $folder"
      errors=$((errors+1))
    fi
  done

  if [ "$errors" -gt 0 ]; then
    echo "❌ $errors project folder(s) are missing required files."
    exit 1
  fi
fi

read -p "Continue? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
  echo "❌ Cancelled."
  exit 1
fi

# Setup virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install dependencies
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Run appropriate script
if [ "$MODE" == "1" ]; then
  OUTPUT_DIR="./output"
  mkdir -p "$OUTPUT_DIR"

  CSV="redirects.csv"
  REDIRECTS="_redirects"
  OUTPUT="$OUTPUT_DIR/_redirects_updated"
  DIFF="$OUTPUT_DIR/redirects_diff.html"
  DOMAIN=""

  echo "🚀 Running single-site update..."
  python3 update_netlify_redirects.py \
    --csv "$CSV" \
    --redirects "$REDIRECTS" \
    --output "$OUTPUT" \
    --diff "$DIFF" \
    --domain "$DOMAIN"

  echo "📂 Output written to: $OUTPUT_DIR"

else
  PROJECTS_DIR="./projects"
  DOMAIN=""

  echo "🚀 Running bulk project update..."
  python3 bulk_update_redirects.py \
    --projects-folder "$PROJECTS_DIR" \
    --domain "$DOMAIN"
fi

# Clean up virtual environment
echo "🧹 Cleaning up virtual environment..."
deactivate
rm -rf "$VENV_DIR"
