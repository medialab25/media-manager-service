"""
Application configuration settings.
"""
import json
from pathlib import Path


class Settings:
    """Application settings."""

    def __init__(self):
        self.config_path = Path("config.json")
        self._load_config()

    def _load_config(self):
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                config = json.load(f)
        else:
            config = {
                "port": 5000,
                "host": "0.0.0.0",
                "debug": True,
                "app_name": "Media Manager Service",
                "jellyfin": {"url": "http://localhost:8096", "api_key": ""},
                "merge": {"input_folders": [], "output_folder": ""},
            }
            # Create default config if it doesn't exist
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)

        self.port = config.get("port", 5000)
        self.host = config.get("host", "0.0.0.0")
        self.debug = config.get("debug", True)
        self.app_name = config.get("app_name", "Media Manager Service")
        self.jellyfin_url = config.get("jellyfin", {}).get(
            "url", "http://localhost:8096"
        )
        self.jellyfin_api_key = config.get("jellyfin", {}).get("api_key", "")
        self.merge = config.get("merge", {"input_folders": [], "output_folder": ""})

    def reload(self):
        """Reload configuration from file."""
        self._load_config()


settings = Settings()
