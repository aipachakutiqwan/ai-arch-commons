"""
Start up the handler class
"""
import logging
from typing import Callable, Dict
from fastapi import FastAPI


def _startup_model(app: FastAPI, app_state_vars: Dict) -> None:
    set_app_state_model(app, app_state_vars)
    logging.info("Request handler initialized")


def set_app_state_model(app, app_state_vars):
    app.state.model = app_state_vars


def start_app_handler(app: FastAPI, app_state_vars: Dict) -> Callable:
    """
    Start up the handler class and set it in the FastAPI config.

    Args:
        :param app: FastAPI class

    Returns:
        FastAPI configured
    """
    def startup() -> None:
        logging.info("Running app start handler.")
        _startup_model(app, app_state_vars)

    return startup


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logging.info("Running app shutdown handler.")
        _shutdown_model(app)
    return shutdown
