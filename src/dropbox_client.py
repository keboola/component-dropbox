import logging
import requests
from urllib.parse import urlparse, urlunparse
from keboola.component import UserException


class DropboxClient:
    """Client for downloading files from Dropbox shared links
    and writing output tables & manifests using Keboola SDK.
    """

    def __init__(self, component, config):
        """:param component: Keboola ComponentBase instance
        :param config: Configuration object
        """
        self.component = component
        self.config = config

    def download_all_files(self) -> None:
        """Process all dropbox links from the config:
        - download each file
        - save CSV to data/out/tables
        - write manifest
        """
        for dropbox_link in self.config.links:
            self._download_single_file(dropbox_link)

    def _download_single_file(self, dropbox_link) -> None:
        download_url = str(dropbox_link.download_url)

        if "dl=0" in download_url:
            download_url = download_url.replace("dl=0", "dl=1")
        else:
            download_url += "&dl=1" if "?" in download_url else "?dl=1"

        parsed = urlparse(download_url)
        safe_url = urlunparse(parsed._replace(query=""))

        table_name = dropbox_link.table_name

        table_def = self.component.create_out_table_definition(
            f"{table_name}.csv",
            primary_key=[],
            incremental=False
        )

        logging.info(
            f"Downloading Dropbox file from {safe_url} -> {table_def.full_path}"
        )
        logging.debug(f"Full download URL (debug only): {download_url}")

        try:
            response = requests.get(download_url, stream=True, timeout=300)
            response.raise_for_status()

            with open(table_def.full_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        except requests.RequestException as e:
            logging.error(f"Failed to download Dropbox file: {safe_url}")
            raise UserException(f"Error downloading file: {e}")

        self.component.write_manifest(table_def)

        logging.info(f"Download complete: {table_name}.csv")
