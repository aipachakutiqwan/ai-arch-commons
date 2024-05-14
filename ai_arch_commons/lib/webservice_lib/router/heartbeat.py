"""
Heartbeat router implementation
"""
from fastapi import APIRouter, Depends
from ai_arch_commons.lib.webservice_lib.core.security import is_authenticated
from ai_arch_commons.lib.webservice_lib.model.heartbeat_response import HeartbeatResponse

ROUTER = APIRouter()

@ROUTER.get("/heartbeat", response_model=HeartbeatResponse, name="heartbeat")
def get_heartbeat(_=Depends(is_authenticated)) -> HeartbeatResponse:
    """
    Heartbeat API router implementation

    Returns:
        HeartbeatResult: pydantic heartbeat class
    """
    heartbeat = HeartbeatResponse(is_alive=True)
    return heartbeat
