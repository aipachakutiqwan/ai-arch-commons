import unittest
from unittest.mock import patch, MagicMock

import pytest

from ai_arch_commons.lib.webservice_lib.core import event_handlers


class TestEventHandlers(unittest.TestCase):
    ''' Test class for src.api.core.event_handlers module '''
    
    def test__startup_model(self):
        ''' Test method to cover _startup_model '''
        app = MagicMock()
        config = {}
        app_state_vars = {}
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.event_handlers.set_app_state_model') as _set_app_state_model:
            event_handlers._startup_model(app, app_state_vars)
        _set_app_state_model.assert_called_once()


    @pytest.mark.skip()
    def test__shutdown_model(self):
        ''' Test method to cover _shutdown_model '''
        app = MagicMock()

        event_handlers._shutdown_model(app)
        self.assertIsNone(app.state.model)

    #@pytest.mark.skip()
    def test_start_app_handler(self):
        ''' Test method to cover start_app_handler '''
        app = MagicMock()
        config = {}
        app_state_vars = {}
        event_handlers._startup_model = MagicMock()
        with patch('ai_arch_commons.lib.webservice_lib.core.event_handlers.set_app_state_model') as _set_app_state_model:
            _startup = event_handlers.start_app_handler(app, _set_app_state_model)
        _startup()
        event_handlers._startup_model.assert_called_once_with(app, _set_app_state_model)


    def test_stop_app_handler(self):
        ''' Test method to cover stop_app_handler '''
        app = MagicMock()
        event_handlers._shutdown_model = MagicMock()
        _shutdown = event_handlers.stop_app_handler(app)
        _shutdown()
        event_handlers._shutdown_model.assert_called_once_with(app)

