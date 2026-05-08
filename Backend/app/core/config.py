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
    mongo_db_uri: str
    mongo_db_name: str

    # CORS
    cors_origins: str

def _required(name: str) -> str:
    value: str | None = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}."
           + " Please check your .env file and try again."
        )
    return value

def get_config() -> Config:
    return Config(
        openai_api_key=_required(name="OPENAI_API_KEY"),
        openai_model=_required(name="OPENAI_MODEL"),
        mongo_db_uri=_required(name="MONGO_DB_URI"),
        mongo_db_name=_required(name="MONGO_DB_NAME"),
        cors_origins=_required(name="CORS_ORIGINS"),
    )

config: Config = get_config()