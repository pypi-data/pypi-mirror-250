# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Annotated
from typing import TypeAlias

import fastapi
import fastapi.params
import pydantic
from aiopki.ext import jose
from aiopki.ext.jose import JWT
from aiopki.ext.jose import OIDCToken
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from oauthx.client import Provider
from oauthx.lib.exceptions import TrustIssues
from oauthx.lib.params import HTTPClient


__all__: list[str] = ['IDTokenBearer']


PROVIDERS: dict[str, Provider] = {}
logger: logging.Logger = logging.getLogger('uvicorn')
security = HTTPBearer(auto_error=False)
Credentials: TypeAlias = Annotated[HTTPAuthorizationCredentials | None, fastapi.Depends(security)]


def IDTokenBearer(
    issuer: str,
    required: bool = True,
    max_age: int | None = None
):
    issuers: set[str] = {issuer}

    async def f(bearer: Credentials, request: fastapi.Request, http: HTTPClient):
        audiences: set[str] = {
            f'{request.url.scheme}://{request.url.netloc}',
            f'{request.url.scheme}://{request.url.netloc}{request.url.path}',
        }
        if bearer is None:
            if required:
                raise HTTPException(
                    status_code=401,
                    detail=(
                        "Authentication is required for this endpoint. Provide "
                        "an OpenID Connect ID token using the Authorization "
                        "header and bearer scheme, issued by any of the following "
                        f"providers: {str.join(', ', sorted(issuers))}"
                    )
                )
            return None
        try:
            jws = jose.parse(bearer.credentials)
            id_token = jws.payload(JWT.model_validate)
        except Exception:
            raise HTTPException(
                status_code=403,
                detail="The Authorization header contained an invalid token."
            )
        if not any(map(id_token.validate_iss, issuers)):
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header was issued by an untrusted issuer. Trusted issuers are '
                    f'{str.join(", ", sorted(issuers))}.'
                )
            )

        if not id_token.validate_exp():
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header is expired.'
                )
            )

        if not id_token.validate_nbf(required=False):
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header is expired.'
                )
            )

        if max_age is not None and not id_token.validate_iat(max_age):
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header is too old or did not contain the "iat" claim.'
                )
            )

        if not id_token.validate_aud(audiences):
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header is not intended for this resource server.'
                )
            )

        assert id_token.iss is not None
        if id_token.iss not in PROVIDERS:
            logger.info("Retrieving issuer metadata (issuer: %s)", id_token.iss)
            provider = PROVIDERS[id_token.iss] = Provider.model_validate({
                'iss': id_token.iss
            })
            await provider.discover(http)

        provider = PROVIDERS[id_token.iss]
        if not provider.can_verify_id_token():
            raise HTTPException(
                status_code=503,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header was properly validated but the issuer does not '
                    'provide public keys to verify the signature.'
                )
            )

        is_valid = False
        try:
            await provider.verify_id_token(jws)
            is_valid = True
        except TrustIssues:
            is_valid = False
        if not is_valid:
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Signature (JWS) provided in the Authorization '
                    'header did not verify against the known public keys for its '
                    'issuer.'
                )
            )
        try:
            setattr(request.state, 'id_token', OIDCToken.model_validate(id_token.model_dump()))
        except pydantic.ValidationError:
            raise HTTPException(
                status_code=403,
                detail=(
                    'The JSON Web Token (JWT) provided in the Authorization '
                    'header could be parsed and had a valid signature, but '
                    'is not a valid Open ID Connect ID Token.'
                )
            )
        return getattr(request.state, 'id_token')
            

    return fastapi.Depends(f)