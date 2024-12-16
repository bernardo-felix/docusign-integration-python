import inspect
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from docusign import docusign
from jwt_helpers import get_private_key, create_api_client
from docusign_esign import RecipientViewRequest
from logger_config import DEFAULT_MESSAGE


router = APIRouter()


class GetViewRecipient(BaseModel):
    returnUrl: str
    name: str
    email: str
    userId: str


class Response(BaseModel):
    envelopeId: str
    redirectUrl: str


@router.post("/view/{envelope_id}/recipient")
async def create_recipent(envelope_id: str, info: GetViewRecipient) -> Response:
    try:
        private_key = await get_private_key("./private.key")
        private_key = private_key.encode("ascii").decode("utf-8")

        jwt_args = await docusign.get_token(private_key=private_key)

        api_client = await create_api_client(
            base_path=jwt_args["base_path"], access_token=jwt_args["access_token"]
        )

        recipient_view_request = RecipientViewRequest(
            authentication_method="None",
            client_user_id=info.userId,
            return_url=info.returnUrl,
            user_name=info.name,
            email=info.email,
        )

        return await docusign.create_recipient_view(
            api_client=api_client,
            account_id=jwt_args["api_account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request,
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
