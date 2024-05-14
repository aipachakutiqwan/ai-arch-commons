"""
Test healthy class
"""
from requests.auth import HTTPBasicAuth


def test_health_check(test_client):
    """
    Test healthy check function
    """
    response = test_client.get("/api/heartbeat/heartbeat",
                               auth=HTTPBasicAuth("bla", "bla")
                               )
    assert response.status_code == 200
    assert response.json() == {'is_alive': True}
