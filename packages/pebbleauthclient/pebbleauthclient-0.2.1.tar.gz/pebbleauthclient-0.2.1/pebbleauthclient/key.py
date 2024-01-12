import os.path
import json
import time

import urllib
import urllib.request
from typing import Optional

import pebbleauthclient.constants as constants
from pebbleauthclient.errors import EmptyJWKSRemoteURIError, EmptyJWKSError


def get_jwk_set() -> dict:
    """
    Return all the JWK currently stored in jwks.json file or in the process memory.

    :return: dict
    """

    if local_jwks_expired():
        reset_jwk_set()

    if not os.getenv('PBL_AUTH_JWKS'):
        print("NOTICE: Store JWKS in process environment variable")
        os.environ['PBL_AUTH_JWKS'] = json.dumps(read_jwks())
        os.environ['PBL_JWKS_LAST_UPDATE'] = str(time.time())
    return json.loads(os.getenv('PBL_AUTH_JWKS'))


def import_remote_jwks(remote_location: str) -> None:
    """
    Import the public RSA key from a remote server to the local /var/credentials/auth/jwks.json file.

    :param remote_location: str
    :return: None
    """
    if not os.path.exists(constants.CERTS_FOLDER):
        os.makedirs(constants.CERTS_FOLDER)

    jwks = ""

    for line in urllib.request.urlopen(remote_location):
        jwks += line.decode('utf-8')

    f = open(constants.JWKS_LOCAL_PATH, "w")
    f.write(jwks)
    f.close()


def read_jwks() -> dict:
    """
    Read the public RSA key from /var/credentials/auth/jwks.json and convert it into JWK Set

    :return: dict
    """
    if not os.path.exists(constants.JWKS_LOCAL_PATH):
        if not constants.JWKS_REMOTE_URI:
            raise EmptyJWKSRemoteURIError()
        import_remote_jwks(constants.JWKS_REMOTE_URI)

    with open(constants.JWKS_LOCAL_PATH) as f:
        data = f.read()

    if not data:
        raise EmptyJWKSError()

    return json.loads(data)


def reset_jwk_set() -> None:
    """
    Remove jwks.json file from /var/credentials/auth and empty PBL_AUTH_JWKS environment variable.

    :return: None
    """
    if os.path.exists(constants.JWKS_LOCAL_PATH):
        os.remove(constants.JWKS_LOCAL_PATH)

    if os.getenv('PBL_AUTH_JWKS'):
        del os.environ['PBL_AUTH_JWKS']


def get_jwk_by_id(kid: str, jwks: dict) -> Optional[dict]:
    """
    Get and return a specific JWK from a provided Keys Set identified by a kid

    :param kid: key id to look for
    :param jwks: Full JWK Set
    :return: JWK if found or None
    """

    jwk = None

    for j in jwks['keys']:
        if j['kid'] == kid:
            jwk = j
            break

    return jwk


def local_jwks_expired() -> bool:
    """
    Check if the JWKS stored locally is expired. The local copy of JWKS is considered as expired if
    PBL_JWKS_LAST_UPDATE (env var) + JWKS_EXP_TIME (const) < time.time() (now)

    :return: bool
    """

    last_update = os.getenv('PBL_JWKS_LAST_UPDATE')

    if not last_update:
        return True

    return float(last_update) + constants.JWKS_EXP_TIME < time.time()
