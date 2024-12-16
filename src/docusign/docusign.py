import inspect
from fastapi import HTTPException
from jwt_helpers import get_jwt_token
from config import Settings
from docusign_esign import (
    EnvelopesApi,
    EnvelopeDefinition,
    ApiClient,
    RecipientViewRequest,
    BulkSendingList,
    BulkEnvelopesApi,
    BulkSendRequest,
)
from logger_config import DEFAULT_MESSAGE, get_logger

logger = get_logger(__name__)

SCOPES = ["signature", "impersonation"]

# settings
CONFIG = Settings()


async def get_consent_url():
    try:

        url_scopes = "+".join(SCOPES)

        redirect_uri = "https://developers.docusign.com/platform/auth/consent"
        consent_url = (
            f"https://{CONFIG.DS_AUTHORIZATION_SERVER}/oauth/auth?response_type=code&"
            f"scope={url_scopes}&client_id={CONFIG.DS_CLIENT_ID}&redirect_uri={redirect_uri}"
        )

        return consent_url

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


async def get_token(private_key: str):
    try:
        token_response = await get_jwt_token(
            private_key=private_key,
            scopes=SCOPES,
            auth_server=CONFIG.DS_AUTHORIZATION_SERVER,
            client_id=CONFIG.DS_CLIENT_ID,
            impersonated_user_id=CONFIG.DS_USER_ID,
        )
        access_token = token_response.access_token

        api_client = ApiClient()
        api_client.set_base_path(CONFIG.DS_AUTHORIZATION_SERVER)
        api_client.set_oauth_host_name(CONFIG.DS_AUTHORIZATION_SERVER)

        user_info = api_client.get_user_info(access_token)
        accounts = user_info.get_accounts()
        api_account_id = accounts[0].account_id
        base_path = accounts[0].base_uri + "/restapi"

        return {
            "access_token": access_token,
            "api_account_id": api_account_id,
            "base_path": base_path,
        }

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


async def create_envelop(
    api_client: ApiClient, account_id: str, envelope_definition: EnvelopeDefinition
):
    try:
        envelopes_api = EnvelopesApi(api_client)
        envelope_summary = envelopes_api.create_envelope(
            account_id=account_id, envelope_definition=envelope_definition
        )

        resp = {
            "envelopeId": envelope_summary.envelope_id,
            "userId": "teste",
        }

        return resp

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


async def create_bulk_list(
    api_client: ApiClient, account_id: str, bulk_sending_list: BulkSendingList
):
    try:
        bulk_envelope_api = BulkEnvelopesApi(api_client)
        envelope_summary = bulk_envelope_api.create_bulk_send_list(
            account_id=account_id, bulk_sending_list=bulk_sending_list
        )

        resp = {
            "listId": envelope_summary.list_id,
        }

        return resp

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


async def create_bulk_send(
    api_client: ApiClient,
    account_id: str,
    bulk_send_request: BulkSendRequest,
    bulk_send_list_id: str,
):
    try:
        bulk_envelope_api = BulkEnvelopesApi(api_client)
        envelope_summary = bulk_envelope_api.create_bulk_send_request(
            account_id=account_id,
            bulk_send_request=bulk_send_request,
            bulk_send_list_id=bulk_send_list_id,
        )

        resp = {
            "batchId": envelope_summary.batch_id,
        }

        return resp

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


async def create_recipient_view(
    api_client: ApiClient,
    envelope_id: str,
    account_id: str,
    recipient_view_request: RecipientViewRequest,
):
    try:
        envelopes_api = EnvelopesApi(api_client)

        results = envelopes_api.create_recipient_view(
            account_id=account_id,
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request,
        )

        resp = {
            "envelopeId": envelope_id,
            "redirectUrl": results.url,
        }

        return resp
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


async def create_console_view(
    api_client: ApiClient,
    envelope_id: str,
    account_id: str,
) -> str:
    try:
        envelopes_api = EnvelopesApi(api_client)

        document = envelopes_api.get_document(
            account_id=account_id,
            envelope_id=envelope_id,
            document_id="1",
        )

        return document

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
