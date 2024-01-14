"""
app.py Is the main file of the application.=
"""

from fastapi import FastAPI
from cryptopi_api.api.routes import cryptocurrencies

# Create the FastAPI instance.
app = FastAPI()

# Register the routes.
app.include_router(cryptocurrencies.router, tags=["cryptocurrency"])
