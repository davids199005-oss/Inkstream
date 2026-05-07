import os
from dotenv import load_dotenv
from dataclasses import dataclass

_ = load_dotenv()

@dataclass(frozen=True)
class Config:
    # OpenAI API
    openai_api_key: str
    openai_model: str

    # Database
    mongo_uri: str
    mongo_db_name: str

    # APP
    app_host: str
    app_port: int
    cors_origins: str

def _required(name: str) -> str:
    value: str | None = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}."
            " Please check your .env file and try again."
        )
    return value

def get_config() -> Config:
    return Config(
        openai_api_key=_required(name="OPENAI_API_KEY"),
        openai_model=_required(name="OPENAI_MODEL"),
        mongo_uri=_required(name="MONGO_DB_URI"),
        mongo_db_name=_required(name="MONGO_DB_NAME"),
        app_host=_required(name="HOST"),
        app_port=int(_required(name="PORT")),
        cors_origins=_required(name="CORS_ORIGINS"),
    )

config: Config = get_config()