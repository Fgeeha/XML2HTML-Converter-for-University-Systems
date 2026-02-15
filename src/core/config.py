from pydantic import (
    BaseModel,
    model_validator,
)
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
    date_time_format: str = "%d%m%Y %H-%M-%S"

    use_snils: dict[str, bool] = {
        "bak": True,
        "mag": True,
        "spo": False,
        "asp": False,
    }

    pk_id: dict[str, int] = {
        "bak": 1812524082527334653,
        "mag": 1812595423435682045,
        "spo": 1812599375173644541,
        "asp": 1812594156837662973,
    }

    file_name_enr_recommended: dict[str, str] = {}
    name_pk: dict[str, str] = {}

    @model_validator(mode="after")
    def _compute_derived_fields(self) -> "AppConfig":
        """Вычисляет производные поля на основе pk_id."""
        if not self.file_name_enr_recommended:
            self.file_name_enr_recommended = {
                key: f"enr_recommended_enrollment_list_{pk}.zip"
                for key, pk in self.pk_id.items()
                if key in ("bak", "mag")
            }
        if not self.name_pk:
            self.name_pk = {
                key: f"enr_rating_{pk}"
                for key, pk in self.pk_id.items()
            }
        return self


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
