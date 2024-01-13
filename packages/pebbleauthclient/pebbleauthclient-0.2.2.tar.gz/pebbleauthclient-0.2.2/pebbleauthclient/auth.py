import jwt
import json

from datetime import datetime, timezone

from pebbleauthclient.errors import NotFoundJWKError, NoAlgorithmProvidedError, EmptyTokenError, KidNotProvidedException
from pebbleauthclient.key import get_jwk_set, get_jwk_by_id, reset_jwk_set
from pebbleauthclient.models import PebbleAuthToken
from pebbleauthclient.token_data import get_token_data_from_jwt_payload


def auth(token: str, options: dict = None) -> PebbleAuthToken:
    """
    Authenticate a provided token into and return a valid PebbleAuthToken object

    :param token: str               Incoming token that must be verified
    :param options: dict            Verifying options. Acceptable claims : audience, issuer. Resource API MUST control its
                                    audience name.

    :return: PebbleAuthToken
    """
    jwks = get_jwk_set()
    kid = jwt.get_unverified_header(token).get('kid')

    if not kid:
        raise KidNotProvidedException

    jwk = get_jwk_by_id(kid, jwks)

    # In the case that no jwk has been found for this kid, we should re-check the remote server for new keys.
    if not jwk:
        reset_jwk_set()

        jwks = get_jwk_set()
        jwk = get_jwk_by_id(kid, jwks)

    # After re-check the remote server, if no jwk has been found for the kid, it is not possible de decode the JWT
    if not jwk:
        raise NotFoundJWKError(kid)

    if "alg" not in jwk:
        raise NoAlgorithmProvidedError(kid)

    if not options:
        options = {}

    claims = ['audience', 'issuer']

    for claim in claims:
        options[claim] = options[claim] if claim in options else None

    verif_aud = True if options['audience'] else False
    verif_iss = True if options['issuer'] else False

    key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    data = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[jwk['alg']],
        audience=options['audience'],
        issuer=options['issuer'],
        options={
            "verify_aud": verif_aud,
            "verify_iss": verif_iss
        }
    )

    token_data = get_token_data_from_jwt_payload(data, token)

    return PebbleAuthToken(token_data)


def auth_from_http_headers(headers: dict, options: dict = None) -> PebbleAuthToken:
    """
    Authenticate user using the HTTP Authorization header provided with the request

    The Authorization headers must be written according to the standard :

    - Authorization name with capitalized A
    - Token content must start with "Bearer " string (ex : *Bearer full_token_string*)

    :param headers: dict            All provided headers (including Authorization) in a dict
    :param options: dict            Verifying options. Acceptable claims : audience, issuer. Resource API MUST control its
                                    audience name.

    :return: PebbleAuthToken
    """

    if headers['Authorization']:
        token = headers['Authorization'].replace('Bearer ', "")
        return auth(token, options)

    raise EmptyTokenError()
