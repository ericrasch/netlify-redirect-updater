
# Netlify Redirect Updater

A command-line utility to update destination URLs in a Netlify `_redirects` file using a CSV mapping file.

## Features

- Replaces exact destination URL matches (e.g., `https://domain.com/...`) in `_redirects`
- Preserves formatting and untouched lines
- Generates an HTML diff report for visual QA
- Optional domain restriction (e.g., only replace URLs from `https://your-domain.com`)

## Requirements

- Python 3.7+
- `pandas`

## Installation

Clone the repository:

```bash
git clone git@github.com:ericrasch/netlify-redirect-updater.git
cd netlify-redirect-updater
```

Install dependencies:

```bash
pip install pandas
```

## Checklist before you start
- CSV file: Must have a header row with:
  - Column A = old_url (full URL to match)
  - Column B = new_url (URL to replace it with)
- Netlify _redirects file: Standard format
- Optional: Domain filter (e.g. https://your-domain.com), or generic fallback (any URL starting with https://)

## Usage

```bash
python update_netlify_redirects.py \
  --csv redirects.csv \
  --redirects _redirects \
  --output _redirects_updated \
  --diff redirects_diff.html \
  --domain https://your-domain.com
```

### Arguments

| Flag         | Description                                      | Required |
|--------------|--------------------------------------------------|----------|
| `--csv`      | CSV file with `old_url,new_url` columns          | ✅       |
| `--redirects`| Original Netlify `_redirects` file               | ✅       |
| `--output`   | Path to write the updated `_redirects` file      | ✅       |
| `--diff`     | Path to write the HTML diff                      | ✅       |
| `--domain`   | (Optional) Restrict updates to this domain       | ❌       |

## Output

- Updated `_redirects` file
- Visual HTML diff report

## License

MIT
