import importlib
import logging
import typing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from contract.semantic_lambda import SemanticLambdaInterface
from models.models import LambdaDescriptor

_logger = logging.getLogger(__name__)


class WrapperRequest(BaseModel):
    """Request to the wrapper to `handle_input`."""

    session_id: str = Field()
    inputs: list[str] = Field()
    metadata: dict[str, str] = Field()


class WrapperResponse(BaseModel):
    """Response to the wrapper to `handle_input`."""

    # result from the lambda operations
    result: list[str] = Field()
    # updated metadata
    metadata: dict[str, str] = Field()


def _lambda_path(descriptor: LambdaDescriptor) -> str:
    return f"/v1/{descriptor.app_name}/handle_input"


def _lambda_op(descriptor: LambdaDescriptor, semantic_lambda: SemanticLambdaInterface) -> typing.Callable:
    async def op(request_data: WrapperRequest) -> WrapperResponse:
        _logger.debug(f"app_name={descriptor.app_name} session_id={request_data.session_id} request={request_data}")
        lambda_result = semantic_lambda.handle_input(request_data.metadata, request_data.inputs)
        _logger.debug(f"app_name={descriptor.app_name} result.result={lambda_result[0]}"
                      f" result.metadata={lambda_result[1]}")
        return WrapperResponse(result=lambda_result[0], metadata=lambda_result[1])

    return op


def _lambda_route(descriptor: LambdaDescriptor) -> typing.Callable:
    module = importlib.import_module(descriptor.module)
    clz = getattr(module, descriptor.class_name)
    return _lambda_op(descriptor, clz())


def _add_routes(fast_api: FastAPI, descriptors: list[LambdaDescriptor]) -> FastAPI:
    for descriptor in descriptors:
        fast_api.add_api_route(
            path=_lambda_path(descriptor),
            endpoint=_lambda_route(descriptor),
            methods=["POST"],
            name=descriptor.app_name,
        )
        _logger.info(f"registering route for lambda.name={descriptor.app_name}")

    return fast_api


def create_wrapper(descriptors: list[LambdaDescriptor]) -> FastAPI:
    """Create the FastAPI wrapper that will serve our semantic lambda functions.
    :return: FastAPI with dynamic routes created for each semantic lambda.
    """
    app = FastAPI()
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthcheck")
    def healthcheck():
        # Required for fly.io healthchecks
        return {"status": "ok"}

    return _add_routes(app, descriptors)
