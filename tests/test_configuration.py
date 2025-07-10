import pytest
from configuration import Configuration, UserException

def test_valid_configuration():
    raw_config = {
        "parameters": {
            "dropbox_links": [
                {
                    "download_url": "https://www.dropbox.com/scl/fi/abcd/products.csv?dl=0",
                    "table_name": "products"
                }
            ]
        },
        "action": "run"
    }

    config = Configuration(**raw_config)
    assert config.links[0].table_name == "products"
    assert str(config.links[0].download_url).startswith("https://www.dropbox.com/")

def test_invalid_table_name():
    raw_config = {
        "parameters": {
            "dropbox_links": [
                {
                    "download_url": "https://www.dropbox.com/scl/fi/abcd/products.csv?dl=0",
                    "table_name": "products@#$"
                }
            ]
        }
    }

    with pytest.raises(UserException) as exc_info:
        Configuration(**raw_config)

    assert "contains invalid characters" in str(exc_info.value)
