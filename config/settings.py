import os
import yaml
from pinecone import Pinecone


class AppConfig:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._set_env_variables()
        self.pinecone_client = self._init_pinecone()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Arquivo {self.config_path} não encontrado.")
        
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def _set_env_variables(self):
        required_keys = ["PINECONE_API_KEY", "OPENAI_API_KEY"]

        for key in required_keys:
            if key not in self.config:
                raise KeyError(f"{key} não encontrado no config.yaml")

            os.environ[key] = self.config[key]

    def _init_pinecone(self) -> Pinecone:
        return Pinecone(api_key=os.environ["PINECONE_API_KEY"])