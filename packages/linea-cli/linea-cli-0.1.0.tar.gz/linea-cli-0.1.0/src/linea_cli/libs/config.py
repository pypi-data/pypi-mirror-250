import os
import json
import logging


class Config:
    def __init__(self) -> None:
        self.config = {}
        os.makedirs(self.config_dir, exist_ok=True)

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as config_file:
                try:
                    self.config = json.load(config_file)
                except json.JSONDecodeError as e:
                    logging.error(
                        f"failed to read linea config file: error detected {e}"
                    )

    def save_config(self, config_data: dict):
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

    @property
    def config_file(self) -> str:
        return f"{self.config_dir}/cli.config"

    @property
    def config_dir(self) -> str:
        default_home = os.path.expanduser("~")
        config_home = os.getenv("LINEA_HOME", default_home)
        return os.path.join(config_home, ".linea")

    @property
    def root_url(self) -> str:
        return self.config.get("linea_root_url")

    @property
    def api_token(self) -> str:
        return self.config.get("api_token")

    @property
    def is_valid(self):
        return bool(self.config) and self.root_url and self.api_token


config = Config()
