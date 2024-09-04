from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppConfig(BaseModel):
    debug: bool = False
    """
    False - transferring files to a folder dump
    True - zip archives remain in the root folder
    """
    file_name_enr_recommended_bak: str = (
        "enr_recommended_enrollment_list_1780165749254516989.zip"
    )
    file_name_enr_recommended_mag: str = (
        "enr_recommended_enrollment_list_1780165823923613949.zip"
    )
    dir_name_file_priority: str = "file_priority"
    data_time_format: str = "%d%m%Y %H-%M-%S"
    name_pk: dict = {
        "bak": "enr_rating_1780165749254516989",
        "mag": "enr_rating_1780165823923613949",
        "spo": "enr_rating_1790248022834278653",
        "asp": "enr_rating_1780891192879345917",
    }
    pk_id: dict = {
        "bak": 1780165749254516989,
        "mag": 1780165823923613949,
        "spo": 1790248022834278653,
        "asp": 1780891192879345917,
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file_encoding="utf-8",
    )
    app: AppConfig = AppConfig()


settings = Settings()
