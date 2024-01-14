"""
app.py Is the main file of the application.=
"""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from cryptopi_api.api.routes import cryptocurrencies

# Create the FastAPI instance.
app = FastAPI()

# Allow localhost in CORS policy.
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "detail": "Bad Request"
        }),
    )


# Register the routes.
app.include_router(cryptocurrencies.router, tags=["cryptocurrency"])
