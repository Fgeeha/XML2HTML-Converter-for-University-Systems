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
    dir_name_file_priority: str = "file_priority"
    data_time_format: str = "%d%m%Y %H-%M-%S"
    use_snils: bool = False
    pk_id: dict = {
        "bak": 1812524082527334653,
        "mag": 1812595423435682045,
        "spo": 1812599375173644541,
        "asp": 1812594156837662973,
    }

    file_name_enr_recommended_bak: str = (
        f"enr_recommended_enrollment_list_{pk_id['bak']}.zip"
    )
    file_name_enr_recommended_mag: str = (
        f"enr_recommended_enrollment_list_{pk_id['mag']}.zip"
    )

    name_pk: dict = {
        "bak": f"enr_rating_{pk_id['bak']}",
        "mag": f"enr_rating_{pk_id['mag']}",
        "spo": f"enr_rating_{pk_id['spo']}",
        "asp": f"enr_rating_{pk_id['asp']}",
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
