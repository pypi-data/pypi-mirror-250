# Linen Closet

This module is designed to provide a standalone CLI and Python package to bulk-download Google Sheets to a single JSON file.

## Installation

```bash
pip install linen-closet
```

## Usage

### Python Package

```python
from linen_closet import load_sheets, S3Configuration

load_sheets(
    credentials_file: str = "credentials.json",  # Likely a Google Service Account Credentials file in JSON format
    output_filename: str = "workbook.json",  # Where to write the JSON file
    max_download_concurrency: int = 10,  # How many concurrent downloads to run
    configuration_filename: str = "sheets.yaml",  # A YAML file containing the sheets to download (see example in repo root)
    cache_file: Optional[str] = None,  # An existing output file. If provided, will only download sheets that have changed since the last download. All sheet data will be included in the output file (cached data will be copied over)
    s3_configuration: Optional[S3Configuration] = None,  # If provided, and either `output_filename` or `cache_file` is an S3 URL, will perform actions against the S3 bucket specified here
)
```

### CLI

__TODO__: Add CLI documentation

## License

[Apache 2.0](LICENSE)
