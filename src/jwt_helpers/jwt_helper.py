"""
 code from docusign
"""

import inspect
from docusign_esign import ApiClient
from os import path
import aiofiles
from fastapi import HTTPException

from logger_config import DEFAULT_MESSAGE


async def get_jwt_token(
    private_key, scopes, auth_server, client_id, impersonated_user_id
):
    try:
        api_client = ApiClient()
        api_client.set_base_path(auth_server)
        response = api_client.request_jwt_user_token(
            client_id=client_id,
            user_id=impersonated_user_id,
            oauth_host_name=auth_server,
            private_key_bytes=private_key,
            expires_in=4000,
            scopes=scopes,
        )

        return response
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


async def get_private_key(private_key_path):
    try:
        private_key_file = path.abspath(private_key_path)

        if path.isfile(private_key_file):
            async with aiofiles.open(private_key_file) as private_key_file:
                private_key = await private_key_file.read()
        else:
            private_key = private_key_path

        return private_key

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


async def create_api_client(base_path, access_token):
    try:
        api_client = ApiClient()
        api_client.host = base_path
        api_client.set_default_header(
            header_name="Authorization", header_value=f"Bearer {access_token}"
        )

        return api_client

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
