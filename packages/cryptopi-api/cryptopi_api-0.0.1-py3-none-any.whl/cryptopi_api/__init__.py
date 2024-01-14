from cryptopi_api.app import app
from cryptopi_api.utils import run_api_locally


def run(host: str = "localhost", port: int = 8000, log_level: str = "info"):
    """
    This function starts the API.
    :return:
    """

    run_api_locally(
        app=app,
        host=host,
        port=port,
        log_level=log_level
    )
