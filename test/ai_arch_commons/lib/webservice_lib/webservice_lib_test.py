from unittest.mock import MagicMock

from ai_arch_commons.lib.webservice_lib.webservice_class import WebServiceLib


def test_webservice_setup_service():
    WebServiceLib.get_router = MagicMock()
    WebServiceLib.get_webserver = MagicMock()
    WebServiceLib.set_router_in_webserver = MagicMock()
    WebServiceLib.add_event_handler = MagicMock()

    webservice_lib = WebServiceLib()
    webservice_lib.setup_service(config={}, router_info=[], app_state_vars={})
    WebServiceLib.get_router.assert_called_once()
    WebServiceLib.get_webserver.assert_called_once()
    WebServiceLib.set_router_in_webserver.assert_called_once()
    WebServiceLib.add_event_handler.assert_called_once()
