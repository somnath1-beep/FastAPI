from pydantic_settings import BaseSettings,SettingsConfigDict

class Setting(BaseSettings):
    database_url: str
    database_hostname: str
    database_username: str
    database_password: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    model_config=SettingsConfigDict(env_file=".env")
settings=Setting()# type: ignore