import os

os.environ["DISABLE_AUTH"] = "true"

import pytest
from starlette.testclient import TestClient
from ai_arch_commons.lib.webservice_lib.webservice_class import WebServiceLib


config_dict = {
    "app_version": '1.0.0',
    "app_name": 'template-web-service',
    "api_prefix": '/api',
    "is_debug": True,
}


@pytest.fixture()
def test_client():
    webservice_lib = WebServiceLib()
    webservice_lib.setup_service(config=config_dict, router_info=[], app_state_vars={})

    app = webservice_lib.app
    with TestClient(app) as test_client:
        yield test_client
