import unittest
from unittest.mock import patch
from ai_arch_commons.lib.webservice_lib.router import heartbeat


class TestHeartbeat(unittest.TestCase):
    ''' Test class for src.api.router.heartbeat module '''

    def test_get_heartbeat(self):
        ''' Test method to cover get_heartbeat '''
        with\
                patch('ai_arch_commons.lib.webservice_lib.router.heartbeat.HeartbeatResponse') as _HeartbeatResponse:
            ret = heartbeat.get_heartbeat()
        self.assertEqual(ret, _HeartbeatResponse.return_value)
        _HeartbeatResponse.assert_called_once_with(is_alive=True)

