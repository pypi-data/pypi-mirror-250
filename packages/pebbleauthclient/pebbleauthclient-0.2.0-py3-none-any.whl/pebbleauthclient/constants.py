import os

JWKS_REMOTE_URI: str = os.getenv('PBL_JWKS_REMOTE_URI')
"""
Return the location of remote pebble authenticator public keys set (JWKS) as defined in the sys global
environment variables
"""

CERTS_FOLDER: str = "./var/credentials/auth"
"""
Contains the local folder for temporary store authentication credentials. Storing locally the credentials improves
server response.
"""

JWKS_LOCAL_PATH: str = CERTS_FOLDER + "/jwks.json"
"""
Contains the local path for the public keys set (JWKS)
"""

env_exp = os.getenv('PBL_JWKS_EXP_TIME')

JWKS_EXP_TIME: int = int(env_exp) if env_exp else 86400
"""
Duration in seconds after which Keys Set (JWKS) is considered as expired. All local copy of the keys must be destroyed 
and the remote server will be requested to create the new copy. Default value : 86400 sec (one day). This can be changed
by exporting `PBL_JWKS_EXP_TIME` environment variable.

::

    export PBL_JWKS_EXP_TIME=3600

"""
