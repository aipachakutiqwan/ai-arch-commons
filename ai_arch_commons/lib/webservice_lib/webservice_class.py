from typing import Dict, List
from ai_arch_commons.lib.webservice_lib.core.event_handlers import start_app_handler
import uvicorn
from fastapi import FastAPI, APIRouter
from ai_arch_commons.lib.webservice_lib.router import heartbeat


class WebServiceLib():
    def __init__(self, heartbeat_prefix='heartbeat'):
        self.num_workers = None
        self.app = None
        self.router = None
        self.config = None
        self.heartbeat_prefix = heartbeat_prefix

    def get_router(self):
        api_router = APIRouter()
        api_router.include_router(heartbeat.ROUTER, tags=['Heartbeat'], prefix=f'/{self.heartbeat_prefix}')
        self.router = api_router

    def setup_service(self, config: Dict, router_info: List, app_state_vars: Dict):
        self.config = config
        self.get_router()

        for router_val in router_info:
            self.set_router_val(router_val)

        fast_app = self.get_webserver()
        self.set_router_in_webserver(fast_app)
        self.add_event_handler(app_state_vars, fast_app)
        self.app = fast_app

    def add_event_handler(self, app_state_vars, fast_app):
        fast_app.add_event_handler('startup', start_app_handler(fast_app, app_state_vars))

    def set_router_in_webserver(self, fast_app):
        fast_app.include_router(self.router, prefix=self.config['api_prefix'])

    def get_webserver(self):
        return FastAPI(title=self.config['app_name'], version=self.config['app_version'],
                       debug=self.config['is_debug'])

    def set_router_val(self, router_val):
        self.router.include_router(router_val[0], tags=router_val[1], prefix=router_val[2])

    def run_service(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8080, workers=self.num_workers, log_level="info")
