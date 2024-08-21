import typing

import httpx

from configs import AuthConfig


class AuthClient(typing.Protocol):
    auth_config: AuthConfig

    async def get_auth_metadata(self) -> tuple[tuple[str, str], ...]:
        pass


class SfAuthClient(AuthClient):
    auth_config: AuthConfig

    def __init__(self, auth_config: AuthConfig) -> None:
        self.auth_config = auth_config

    async def get_auth_metadata(self) -> tuple[tuple[str, str], ...]:
        async with httpx.AsyncClient() as client:
            auth_params = {
                'client_id': self.auth_config.client_id,
                'client_secret': self.auth_config.client_secret,
                'grant_type': 'client_credentials'
            }

            resp = await client.post(
                url=self.auth_config.auth_endpoint,
                params=auth_params
            )

            resp.raise_for_status()

            return self.process_access_token_response(resp)

    def process_access_token_response(self, resp: httpx.Response) -> tuple[tuple[str, str], ...]:
        resp_dict = resp.json()

        access_token = resp_dict.get('access_token')
        instance_url = resp_dict.get('instance_url')
        org_id = resp_dict.get('id').split('/')[4:5][0]

        return (
            ('accesstoken', access_token),
            ('instanceurl', instance_url),
            ('tenantid', org_id)
        )
