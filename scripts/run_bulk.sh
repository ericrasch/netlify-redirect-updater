#!/bin/bash

# Bulk redirect update for all projects inside the specified folder

PROJECTS_DIR="./projects"
DOMAIN="https://your-domain.com"

python3 bulk_update_redirects.py \
  --projects-folder "$PROJECTS_DIR" \
  --domain "$DOMAIN"
