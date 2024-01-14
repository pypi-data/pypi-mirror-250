"""
utils.py This file contains the utility functions.
"""

import uvicorn
from fastapi import FastAPI


def run_api_locally(app: FastAPI, host: str = "localhost", port: int = 8000, log_level: str = "info"):
    """
    This function runs the API locally.
    :return:
    """

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=log_level
    )
