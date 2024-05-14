from unittest.mock import patch, MagicMock
from ai_arch_commons.lib.ai_app_lib.ai_app_class import AIApp


class DummyClass:
    def __init__(self):
        self.config = None
        pass

    def setup_from_config(self, config):
        self.config = config

    def run_service(self, ):
        pass


def test_ai_app_setup_service_object():
    config_dict = {
        "service_module_path": "bla",
        "service_class": "bla",
        "service_config": {"bla"}
    }
    ai_app = AIApp()
    ai_app.config = config_dict
    AIApp.get_service_obj = MagicMock(return_value = DummyClass())

    with (
        patch("importlib.import_module") as import_module_patch,
    ):
        import_module_patch.return_value = "dummy_module"
        ai_app.setup_service_obj()
        assert isinstance(ai_app.service_obj, DummyClass)


def test_ai_app_run_service():
    config_dict = {
        "service_module_path": "bla",
        "service_class": "bla",
        "service_config": {"bla"}
    }
    ai_app = AIApp()
    ai_app.config = config_dict
    ai_app.service_obj = DummyClass()
    ai_app.service_obj.run_service = MagicMock(return_value=1)
    ai_app.run_service()
    ai_app.service_obj.run_service.assert_called_once()


def test_ai_app_setup_config_and_log():
    ai_app = AIApp()
    ai_app.get_app_config_params = MagicMock()
    ai_app.config_logger = MagicMock()
    ai_app.setup_config_and_log()

    ai_app.get_app_config_params.assert_called_once()
    ai_app.config_logger.assert_called_once()


