# Dropbox Extractor (API v2 using Python)

The Dropbox Extractor automates downloading files from public Dropbox share links directly into Keboola Storage.

## Features

- **Download via Share Links**
  - Accepts one or multiple Dropbox share URLs.

- **CSV Table Output**
  - Saves downloaded files as CSV tables in `/data/out/tables/`.
  - Generates Keboola Storage manifests automatically.

- **Custom Bucket Support**
  - Users can optionally define a custom bucket name for output tables.
  - Defaults to `in.c-dropbox-extractor`.

- **Secure Logging**
  - Logs only safe parts of Dropbox URLs.
  - Prevents sensitive tokens from appearing in logs.

- **Modern Migration Path**
  - Designed to replace older Dropbox extractors written in Node.js.
  - Supports similar configuration structures for easy migration.


## Configuration

The extractor requires a JSON configuration file structured like this:

```json
{
  "parameters": {
    "dropbox_links": [
      {
        "download_url": "https://www.dropbox.com/scl/fi/xtks1q4d3hfwvy01hhm43/products.csv?dl=0",
        "table_name": "products"
      }
    ],
    "bucket": "in.c-dropbox-extractor",
    "debug": false
  },
  "action": "run"
}
```

### Configuration Parameters

| Parameter       | Required | Description                                                                                                                             |
| --------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `dropbox_links` | Yes      | An array of Dropbox files to download. Each object requires a `download_url` (Dropbox share link) and `table_name` (output table name). |

#### Important:

- Your Dropbox links should be publicly accessible via a share URL.
- The extractor automatically updates links from `dl=0` to `dl=1` to ensure direct download.
- Table names can only include letters, numbers, dots, underscores, and hyphens.

## Output

After a successful run:

- The downloaded file will be saved as:

```text
/data/out/tables/{table_name}.csv
```

- A manifest file will be generated alongside each table:


```json
{
  "incremental": false,
  "destination": "in.c-dropbox-extractor.{table_name}"
}
```

## Migration from Node.js Extractor

If migrating from the original Node.js Dropbox Extractor:

- Configuration remains largely the same.
- Encrypted URL fields (`#download_url`) have been replaced with plaintext `download_url` for a better UX. The sensitive part of links is not logged anywhere.
- Logging and error handling have been improved.
- Manifests and file locations are consistent with Keboola best practices.

## Running Locally

For local testing, create a `data/config.json` file in your working directory:

```json
{
  "parameters": {
    "dropbox_links": [
      {
        "download_url": "https://www.dropbox.com/scl/fi/xtks1q4d3hfwvy01hhm43/products.csv?dl=0",
        "table_name": "products"
      }
    ]
  }
}
```

Then run:

```bash
python3 src/component.py
```

## Development & Testing

Install requirements:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

## License

MIT License