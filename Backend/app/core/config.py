import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Config:
    # OpenAI API
    openai_api_key: str
    openai_model: str

    # Database
    mongo_uri: str
    mongo_db_name: str

    # APP
    app_env: str
    app_host: str
    app_port: int
    cors_origins: str

def _required(value: str) -> str:
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {value}."
            +  "Please check your .env file and try again."
        )
    return value

def get_config() -> Config:
    return Config(
        openai_api_key=_required(value="OPENAI_API_KEY"),
        openai_model=_required(value="OPENAI_MODEL"),
        mongo_uri=_required(value="MONGO_URI"),
        mongo_db_name=_required(value="MONGO_DB_NAME"),
        app_env=_required(value="APP_ENV"),
        app_host=_required(value="APP_HOST"),
        app_port=int(_required(value="APP_PORT")),
        cors_origins=_required(value="CORS_ORIGINS"),
    )

config: Config = get_config()