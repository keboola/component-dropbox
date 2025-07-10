import pytest
import io
from unittest.mock import patch, MagicMock
from configuration import Configuration
from dropbox_client import DropboxClient


@pytest.fixture
def mock_component(tmp_path):
    component = MagicMock()

    def create_out_table_definition(filename, primary_key, incremental):
        class TableDef:
            full_path = tmp_path / filename
        return TableDef()

    component.create_out_table_definition.side_effect = create_out_table_definition
    return component


@patch("dropbox_client.requests.get")
def test_download_single_file(mock_requests_get, mock_component, tmp_path):
    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"some,data\n1,2\n"]
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    raw_config = {
        "parameters": {
            "dropbox_links": [
                {
                    "download_url": "https://www.dropbox.com/scl/fi/abcd/products.csv?dl=0",
                    "table_name": "products"
                }
            ]
        }
    }

    config = Configuration(**raw_config)
    client = DropboxClient(mock_component, config)

    client.download_all_files()

    output_path = tmp_path / "products.csv"
    assert output_path.exists()
    assert "some,data" in output_path.read_text()

    assert mock_component.write_manifest.called
    mock_requests_get.assert_called_once()
