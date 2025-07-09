import pytest
from pydantic import ValidationError
from configuration import Configuration, UserException

def test_valid_configuration():
    raw_config = {
        "parameters": {
            "dropbox_links": [
                {
                    "download_url": "https://www.dropbox.com/scl/fi/abcd/products.csv?dl=0",
                    "table_name": "products"
                }
            ],
            "bucket": "in.c-my_bucket",
            "debug": False
        },
        "action": "run"
    }

    config = Configuration(**raw_config)
    assert config.bucket_name == "in.c-my_bucket"
    assert config.links[0].table_name == "products"

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

def test_invalid_bucket_name():
    raw_config = {
        "parameters": {
            "dropbox_links": [
                {
                    "download_url": "https://www.dropbox.com/scl/fi/abcd/products.csv?dl=0",
                    "table_name": "products"
                }
            ],
            "bucket": "invalidbucket"
        }
    }

    with pytest.raises(UserException) as exc_info:
        Configuration(**raw_config)

    assert "should contain a dot" in str(exc_info.value)
