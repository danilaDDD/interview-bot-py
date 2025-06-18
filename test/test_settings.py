from app.setting.setting import Settings
from .conftest import *

@pytest.mark.system
@pytest.mark.local
class TestSettings:
    def test_load_settings(self, test_settings: Settings):
        assert test_settings.ENV == 'test'
        assert "test" in test_settings.DB_NAME
        assert len(test_settings.get_database_url()) > 0