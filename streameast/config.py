from dataclasses import dataclass
import yaml
from typing import ClassVar, Optional

@dataclass
class App:
    id: str
    secret: str

@dataclass
class Config:
    raffle_message: str
    app: App

    conf: ClassVar[Optional[Config]] = None

    @staticmethod
    def get():
        if Config.conf is None:
            with open('./config.yaml') as f:
                yaml_dict: dict = yaml.safe_load(f)
                yaml_dict['app'] = App(**yaml_dict['app'])
                Config.conf = Config(**yaml_dict)
        return Config.conf