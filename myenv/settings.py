from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict(myenv_file="myenv",extra="ignore")
    DB_CONNECTION:str= "sqlite:///./app.db"

DB_CONNECTION:str
SECRET_KEY:str
ALGORITHM:str
EXP_TIME:int

settings=Settings()
