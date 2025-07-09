"""
Dropbox Extractor Component (v2) main class.
"""
from datetime import datetime, UTC
import logging
from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from configuration import Configuration
from dropbox_client import DropboxClient


class Component(ComponentBase):
    def __init__(self):
        super().__init__()

    def run(self):
        run_time = datetime.now(UTC)
        run_time_str = run_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        raw_config = {
            "parameters": self.configuration.parameters,
            "action": getattr(self.configuration, "action", "run")
        }

        config = Configuration(**raw_config)
        client = DropboxClient(self, config)
        client.download_all_files()

        new_state = {
            "last_successful_run": run_time_str
        }

        logging.info("Saving component state...")
        self.write_state_file(new_state)
        logging.info("Data processing completed!")


"""
Main entrypoint
"""
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        comp = Component()
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
