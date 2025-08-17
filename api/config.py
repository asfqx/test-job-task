from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASS: str
    POSTGRES_DB_NAME: str
    DB_DIALECT: str = "postgresql+asyncpg"
    REDIS_HOST: str
    REDIS_PORT: str
    API_KEY: str

    @property
    def db_url(self) -> str:
        return (
            f"{self.DB_DIALECT}://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASS}@{self.POSTGRES_DB_HOST}:"
            f"{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"
        )

    class Config:
        env_file = "./.env"


settings = Settings()
