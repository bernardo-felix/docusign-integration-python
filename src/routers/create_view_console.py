import inspect
from fastapi import APIRouter, HTTPException
from docusign import docusign
from jwt_helpers import get_private_key, create_api_client
from fastapi.responses import FileResponse
from logger_config import DEFAULT_MESSAGE

router = APIRouter()


@router.get("/view/{envelope_id}/console", response_class=FileResponse)
async def create_console(envelope_id: str) -> FileResponse:
    try:
        private_key = await get_private_key("./private.key")
        private_key = private_key.encode("ascii").decode("utf-8")

        jwt_args = await docusign.get_token(private_key=private_key)

        api_client = await create_api_client(
            base_path=jwt_args["base_path"], access_token=jwt_args["access_token"]
        )

        return await docusign.create_console_view(
            api_client=api_client,
            account_id=jwt_args["api_account_id"],
            envelope_id=envelope_id,
        )

    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(
            500,
            {
                "func": inspect.currentframe().f_code.co_name,
                "err": str(err),
                "message": DEFAULT_MESSAGE,
            },
        )
