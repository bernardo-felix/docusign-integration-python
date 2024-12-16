import inspect
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from jwt_helpers import get_private_key, create_api_client
from docusign import docusign
from docusign_esign import BulkSendRequest
from logger_config import DEFAULT_MESSAGE


router = APIRouter()


class CreateSendBulk(BaseModel):
    templateId: str
    listId: str
    batchName: str


class Response(BaseModel):
    batchId: str


@router.post("")
async def create_bulk_list(infos: CreateSendBulk) -> Response:
    try:
        private_key = await get_private_key("./private.key")
        private_key = private_key.encode("ascii").decode("utf-8")

        jwt_args = await docusign.get_token(private_key=private_key)

        api_client = await create_api_client(
            base_path=jwt_args["base_path"], access_token=jwt_args["access_token"]
        )

        bulk_send_request = BulkSendRequest(
            envelope_or_template_id=infos.templateId,
            batch_name=infos.batchName,
        )
        return await docusign.create_bulk_send(
            api_client=api_client,
            account_id=jwt_args["api_account_id"],
            bulk_send_request=bulk_send_request,
            bulk_send_list_id=infos.listId,
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
