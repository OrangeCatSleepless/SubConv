from typing import List, Tuple
from pathlib import Path
import sys

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource

from . import config_template


class Group(BaseModel):
    name: str
    type: str
    rule: bool = True
    manual: bool = False
    prior: str = None
    regex: str = None


class Config(BaseSettings):
    HEAD: dict
    TEST_URL: str = "http://www.gstatic.com/generate_204"
    RULESET: List[Tuple[str, str]] = []
    CUSTOM_PROXY_GROUP: List[Group] = []

    model_config = SettingsConfigDict(yaml_file="config.yaml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


try:
    if Path("config.yaml").exists():
        with open("config.yaml", "r", encoding="utf-8") as f:
            if f.read() == "":
                raise FileNotFoundError
    configInstance = Config()
except FileNotFoundError:
    print(
        f"config.yaml not found or empty, please run {sys.argv[0]} -h to see how to generate a default config file"
    )
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
