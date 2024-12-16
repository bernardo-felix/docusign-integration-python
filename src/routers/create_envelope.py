import inspect
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from jwt_helpers import get_private_key, create_api_client
from docusign import docusign
from docusign_esign import (
    Text,
    Tabs,
    TemplateRole,
    EnvelopeDefinition,
)
from logger_config import DEFAULT_MESSAGE


router = APIRouter()


class UserInfos(BaseModel):
    name: str
    email: EmailStr
    userId: str
    params: Optional[dict[str, str]]


class CreateEnvelope(BaseModel):
    templateId: str
    users: list[UserInfos]


class Response(BaseModel):
    envelopeId: str


@router.post('')
async def create_envelope(infos: CreateEnvelope) -> Response:
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
                text_tabs.append(Text(tab_label=key, value=value))
            tabs = Tabs(text_tabs=text_tabs)

            template_roles.append(
                TemplateRole(
                    email=user.email,
                    name=user.name,
                    role_name="signer",
                    client_user_id=user.userId,
                    tabs=tabs,
                )
            )

        envelope_definition = EnvelopeDefinition(
            template_id=infos.templateId,
            status="sent",
            template_roles=template_roles,
        )

        return await docusign.create_envelop(
            api_client=api_client,
            account_id=jwt_args["api_account_id"],
            envelope_definition=envelope_definition,
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
