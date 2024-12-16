import importlib
import pkgutil

from fastapi.routing import APIRoute
import routers
from fastapi import FastAPI, Request, HTTPException
from config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from logger_config import get_logger
from fastapi.exceptions import RequestValidationError


app = FastAPI()
logger = get_logger(__name__)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# exception from validation params
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    body = await request.body()
    body_content = body.decode("utf-8") if body else "Empty body"

    dict = {
        "status": 400,
        "body": body_content,
        "query": request.query_params,
        "params": request.path_params,
        "error": str(exc),
        "route": f"{request.url}",
    }

    logger.error("Parametros Não aceitos", extra=dict)
    return JSONResponse(
        content={
            "message": "parametros não aceitos",
            "err": str(exc),
            "route": f"{request.url}",
        },
        status_code=400,
    )


# exception from http
@app.exception_handler(HTTPException)
async def log_exception_handle(request: Request, exc: HTTPException):

    message = exc.detail["message"]
    err = exc.detail["err"]
    func = exc.detail["func"]

    body = await request.body()
    body_content = body.decode("utf-8") if body else "Empty body"

    dict = {
        "status": exc.status_code,
        "body": body_content,
        "query": request.query_params,
        "params": request.path_params,
        "error": err,
        "func": func,
        "route": f"{request.url}",
    }

    logger.error(message, extra=dict)
    return JSONResponse(
        content={
            "message": message,
            "err": err,
            "func": func,
            "route": f"{request.url}",
        },
        status_code=exc.status_code,
    )


# @app.middleware("http") #ativar junto com aumento de plano do betterstack
# async def log_middleware(request: Request, call_next):
#     log_dict = {"url": request.url, "method": request.method}
#     logger.info("API REQUEST", extra=log_dict)

#     response = await call_next(request)
#     return response


def get_settings() -> Settings:
    return Settings()


for _, module_name, _ in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f"routers.{module_name}")
    if hasattr(module, "router"):
        route = "".join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(module_name.split("_"))
        )
        app.include_router(module.router, prefix=f"/{route}", tags=[module_name])


for route in app.routes:
    if isinstance(route, APIRoute):
        methods = ", ".join(route.methods)
        logger.info(f"{methods} {route.path} -> {route.name}")
