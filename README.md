
# Netlify Redirect Updater

A command-line utility to update destination URLs in Netlify `_redirects` files using CSV mapping files. Supports both **single-site updates** and **bulk project folder processing** via an interactive shell script.

---

## ✅ Features

- Updates only exact matches to avoid unintentional changes
- Preserves formatting and untouched lines
- Visual HTML diff report for QA
- Supports per-project folder structure for bulk processing
- Virtual environment setup and dependency installation handled automatically
- Interactive CLI with built-in pre-checks

---

## 🏁 Quick Start (Recommended)

```bash
./run_script.sh
```

This launches an interactive prompt to choose between:

1. Single-site update
2. Bulk project update

The script:
- Checks for required files
- Creates a virtual environment (if needed)
- Installs `pandas`
- Runs the appropriate updater

---

## 📁 Folder Structure

### Single-site:
```
/your-folder/
  redirects.csv
  _redirects
```

### Bulk (multi-project):
```
/projects/
  /site-a/
    redirects.csv
    _redirects
  /site-b/
    redirects.csv
    _redirects
```

---

## 🧪 CSV Format

Your `redirects.csv` must have a header:

```
old_url,new_url
https://your-site.com/old-path,https://your-site.com/new-path
```

---

## ⚙️ Dependencies

- Python 3.7+
- `pandas` (auto-installed when running `run_script.sh`)
- Works best in Unix-like environments (macOS, Linux)

---

## 📂 Included Files

| File | Purpose |
|------|---------|
| `run_script.sh` | Interactive runner for both modes |
| `update_netlify_redirects.py` | Single-site updater |
| `bulk_update_redirects.py` | Bulk folder updater |
| `requirements.txt` | Python dependency list |
| `/examples/` | Sample `_redirects` and `redirects.csv` files |

---

## 📝 License

MIT — Eric Rasch  
https://github.com/ericrasch/netlify-redirect-updater
