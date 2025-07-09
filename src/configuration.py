import logging
import re
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, model_validator
from keboola.component.exceptions import UserException


class DropboxLink(BaseModel):
    download_url: HttpUrl = Field(
        ...,
        title="Dropbox Download URL",
        description="Paste the Dropbox share link to download your file."
    )
    table_name: str = Field(
        ...,
        title="Table Name",
        description="Name of the output table in Keboola Storage."
    )

    @model_validator(mode="after")
    def validate_table_name(self) -> "DropboxLink":
        if not self.table_name.strip():
            raise ValueError("table_name cannot be empty")

        if not re.match(r"^[a-zA-Z0-9_.-]+$", self.table_name):
            raise ValueError(
                f"table_name '{self.table_name}' contains invalid characters. "
                "Only letters, numbers, underscores, hyphens, and dots are allowed."
            )
        return self


class Parameters(BaseModel):
    dropbox_links: List[DropboxLink] = Field(
        ...,
        title="Dropbox Links",
        description="List of Dropbox links to download and corresponding table names."
    )
    bucket: Optional[str] = Field(
        "in.c-dropbox-extractor",
        title="Bucket Name",
        description="Optional. Bucket where all downloaded tables will be stored."
    )
    debug: bool = Field(
        False,
        title="Enable Debug Mode",
        description="Enable verbose logging for debugging purposes."
    )

    @model_validator(mode="after")
    def validate_bucket(self) -> "Parameters":
        if self.bucket is not None:
            self.bucket = self.bucket.strip()
            if not self.bucket:
                raise ValueError("Bucket name cannot be empty if provided.")
            if "." not in self.bucket:
                raise ValueError(
                    f"Bucket name '{self.bucket}' is invalid. It should contain a dot (e.g. 'in.c-my_bucket')."
                )
        return self


class Configuration(BaseModel):
    parameters: Parameters
    action: Optional[str] = Field(default="run")

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:
            error_messages = [
                f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                for err in e.errors()
            ]
            raise UserException(
                f"Configuration validation error: {', '.join(error_messages)}"
            )

        if self.parameters.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(message)s",
            )
            logging.debug("Component will run in Debug mode")
            logging.debug("Resolved configuration:")
            logging.debug(self.model_dump_json(indent=2))

    @property
    def bucket_name(self) -> str:
        return self.parameters.bucket or "in.c-dropbox-extractor"

    @property
    def links(self) -> List[DropboxLink]:
        return self.parameters.dropbox_links
