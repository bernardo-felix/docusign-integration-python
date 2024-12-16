import inspect
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from jwt_helpers import get_private_key, create_api_client
from docusign import docusign
from docusign_esign import (
    BulkSendingCopy,
    BulkSendingList,
    BulkSendingCopyRecipient,
    BulkSendingCopyTab,
)
from logger_config import DEFAULT_MESSAGE


router = APIRouter()


class UserInfos(BaseModel):
    name: str
    email: EmailStr
    userId: str
    params: Optional[dict[str, str]]


class CreateEnvelope(BaseModel):
    listName: str
    users: list[UserInfos]


class Response(BaseModel):
    listId: str


@router.post("")
async def create_send_bulk(infos: CreateEnvelope) -> Response:
    try:
        private_key = await get_private_key("./private.key")
        private_key = private_key.encode("ascii").decode("utf-8")

        jwt_args = await docusign.get_token(private_key=private_key)

        api_client = await create_api_client(
            base_path=jwt_args["base_path"], access_token=jwt_args["access_token"]
        )

        template_roles = []
        for user in infos.users:
            text_tabs = []
            for key, value in user.params.items():
                text_tabs.append(BulkSendingCopy(tab_label=key, initial_value=value))
            tabs = BulkSendingCopyTab(text_tabs=text_tabs)

            recipient = BulkSendingCopyRecipient(
                client_user_id=user.userId,
                email=user.email,
                name=user.name,
                role_name="Signer",
                tab=tabs,
            )

            template_roles.append(
                BulkSendingCopy(
                    email_subject="Please assign here", recipients=[recipient]
                )
            )

        bulk_sending_list = BulkSendingList(
            name=infos.listName, bulk_copies=template_roles
        )

        return await docusign.create_bulk_list(
            api_client=api_client,
            account_id=jwt_args["api_account_id"],
            bulk_sending_list=bulk_sending_list,
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
