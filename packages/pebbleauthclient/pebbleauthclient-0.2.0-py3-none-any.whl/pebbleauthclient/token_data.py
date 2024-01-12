from pebbleauthclient.datatypes import AuthenticatedLicenceObject
from pebbleauthclient.datatypes import PebbleTokenData
from pebbleauthclient.datatypes import UserObject
from pebbleauthclient.models.User import User


def get_licence_object_from_token_data(token_data: PebbleTokenData) -> AuthenticatedLicenceObject:
    """
    Provide all token data and generate a new AuthenticatedLicenceObject instance.

    :param token_data: PebbleTokenData . A representation of data provided by a token
    :return: AuthenticatedLicenceObject
    """
    user = User(
        UserObject(
            username=token_data.sub,
            roles=token_data.roles,
            level=token_data.lv,
            display_name=token_data.name,
            scopes=token_data.scope.split(" ") if token_data.scope else []
        )
    )

    return AuthenticatedLicenceObject(
        app=token_data.client_id,
        issuer=token_data.iss,
        tenant_id=token_data.tid,
        user=user
    )


def get_token_data_from_jwt_payload(jwt_payload: dict, token: str) -> PebbleTokenData:
    """
    Generated a PebbleTokenData instance from a dict representation of the JWT and the token string.

    :param jwt_payload: dict of the information stored in the token
    :param token: str original JWT
    :return: PebbleTokenData
    """

    claims = ('aud', 'iss', 'tid', 'sub', 'roles', 'lv', 'name', 'iat', 'exp', 'scope', 'jti', 'client_id')

    for claim in claims:
        if claim not in jwt_payload:
            jwt_payload[claim] = None

    return PebbleTokenData(
        aud=jwt_payload['aud'],
        iss=jwt_payload['iss'],
        tid=jwt_payload['tid'],
        sub=jwt_payload['sub'],
        roles=jwt_payload['roles'],
        lv=jwt_payload['lv'],
        name=jwt_payload['name'],
        iat=jwt_payload['iat'],
        exp=jwt_payload['exp'],
        scope=jwt_payload['scope'],
        jti=jwt_payload['jti'],
        client_id=jwt_payload['client_id'],
        token=token
    )
