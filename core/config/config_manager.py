import json
from pathlib import Path


class ConfigManager:
    __instance = None
    folder_path = Path("config")
    file_path = folder_path.joinpath("acgcag_config.json")

    def __init__(self, config_data: dict):
        self._has_run_setup: bool = config_data["has_run_setup"]

    @property
    def has_run_setup(self):
        return self._has_run_setup

    def completed_setup(self):
        self._has_run_setup = True
        self.save()

    @staticmethod
    def setup():
        return ConfigManager.__instance or ConfigManager.__setup()

    @staticmethod
    def __setup():
        if ConfigManager.folder_path.exists() and ConfigManager.file_path.exists():
            with open(ConfigManager.file_path, "r", encoding="utf-8") as f:
                return ConfigManager(json.load(f))

        ConfigManager.__instance = ConfigManager({"has_run_setup": False})
        ConfigManager.__instance.save()

        return ConfigManager.__instance

    def save(self):
        """
        Save the config with the existing values to disk.
        """

        if not ConfigManager.folder_path.exists():
            ConfigManager.folder_path.mkdir()

        with open(ConfigManager.file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_dict()))

    def to_dict(self):
        """
        Returns all available configs as a `dict`.
        """

        return {"has_run_setup": self._has_run_setup}
