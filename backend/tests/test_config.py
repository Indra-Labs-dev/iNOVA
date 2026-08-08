from app.core.config import PROJECT_AUTHOR, PROJECT_AUTHOR_ID, PROJECT_NAME, get_settings


def test_project_identity_constants():
    assert PROJECT_NAME == "iNOVA"
    assert PROJECT_AUTHOR == "Archange Elie Yatte"
    assert PROJECT_AUTHOR_ID == "AEY"


def test_settings_loads_with_defaults():
    settings = get_settings()
    assert settings.api_v1_prefix == "/api/v1"
    assert settings.jwt_algorithm == "HS256"


def test_settings_is_cached():
    # get_settings is @lru_cache'd — same object every call within a process.
    assert get_settings() is get_settings()
