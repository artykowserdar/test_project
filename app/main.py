from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from . import models, schemas
from .database import engine
from .routers import users, token

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Taxi admin backend",
    description="Backend for Taxi",
    version="1.0.0"
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid!")


@AuthJWT.load_config
def get_config():
    return schemas.JWTSettings()


async def authjwt_exception_handler(exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.exception_handler(AuthJWTException)

app.include_router(
    token.router,
    prefix="/api",
    tags=["Token"],
    responses={404: {"description": "Not Found!"}}
)

app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "Not Found!"}}
)
