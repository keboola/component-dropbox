Configure the Dropbox Extractor by specifying one or more Dropbox share links and how you’d like the resulting files stored in Keboola.

- **Dropbox Links** (Required)  
  Add one or more entries, each with:
    - **Download URL**: A public Dropbox share link to the file you want to download.  
    - **Table Name**: The name for the output table in Keboola Storage. Only letters, numbers, dots, underscores, and hyphens are allowed.

- **Bucket** (Optional)  
  Define the Storage bucket where your tables should be saved (e.g. `in.c-my_bucket`). If left blank, the extractor uses a default bucket.

- **Enable Debug Mode** (Optional)  
  Enable to produce detailed logs for troubleshooting.

All files are saved as CSV tables in Keboola Storage, with automatically generated manifests. Ensure your Dropbox links are accessible via public sharing and end with `dl=0` or similar. The extractor will automatically adjust the link for download.
