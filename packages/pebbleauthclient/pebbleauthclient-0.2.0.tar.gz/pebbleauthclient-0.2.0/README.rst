Quickstart
==========

Introduction
------------

This library offer a client for authenticate user and licence management
written in Python compatible with may python API Server.

Installation
------------

Requirements
~~~~~~~~~~~~

The following procedures explains the installation of the following packages :

- Python 3.9 or higher
- pip (provided with Python package)
- PyJWT (tested with version 2.8.0)
- cryptography (tested with version 41.0.5)

Solution 1 : requirement.txt configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your project use a requirement.txt configuration file, simply add the
following.

requirement.txt file addition::

    pebbleauthclient>=0.2.0

Then run this command on your project :

::

    pip install -r requirements.txt

Or in Dockerfile :

.. code:: Dockerfile

    RUN pip install -r requirements.txt

Solution 2 : Local installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check python3 is properly installed on your local machine (with pip working),
then run the following in the application directory.

::

    pip install pebbleauthclient

Or in Dockerfile :

.. code:: Dockerfile

    RUN pip install pebbleauthclient

.. note::

    We suggest to use the requirement.txt solution if you are using Docker.

Usage
-----

Configuration
~~~~~~~~~~~~~

Before you can work with the library, you must define to a system environment
variable the URI were is stored the public Json Web Key Set (JWKS file).

This file will be requested and store **temporary** on your API Server.
Your server should be able to write on *./var/credentials/auth/jwks.json* .
If the file does not exist, it will be created.

**If you start your server directly from a terminal, run this command on
your terminal before starting your server :**

::

    export PBL_JWKS_REMOTE_URI=https://SERVER_URI/path/jwks.json

**If you start your server within a Docker container, you should add this
line to your Dockefile :**

.. code:: Dockerfile

    ENV PBL_JWKS_REMOTE_URI=https://SERVER_URI/path/jwks.json

Test keys pair
~~~~~~~~~~~~~~

.. attention::
    These key files are not secured and must be used FOR TESTING PURPOSE
    ONLY on a local development environment !

**JWKS URI (for PBL_JWKS_REMOTE_URI environment variable)**

https://storage.googleapis.com/pebble-public-cdn/test_auth/jwks_test.json

**Public and private keys used to sign a token**

https://storage.googleapis.com/pebble-public-cdn/test_auth/public_test.pem

https://storage.googleapis.com/pebble-public-cdn/test_auth/private_test.pem

Authenticate with token string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pebbleauthclient.auth import auth

    try:
        authToken = auth("---A_valid_token---")

        print(authToken)
        print(authToken.get_user())
        print(authToken.get_authenticated_licence())
    except Exception as e:
        print("ERROR: " + e)

Authenticate with HTTP Authorization header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    This example shows one way to serverside authenticate a user with the Authorization
    header. The important thing is to communicate a dict to ``auth_from_http_headers()``
    function with a valid Authorization key value.

.. code:: python

    from http.server import HTTPServer, BaseHTTPRequestHandler
    from pebbleauthclient.auth import auth_from_http_headers


    class HandleRequest(BaseHTTPRequestHandler):

        def do_GET(self):
            try:
                auth_token = auth_from_http_headers(self.headers)
                licence = auth_token.get_authenticated_licence()
                user = auth_token.get_user()

                print(licence)
                print(user)

                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()

                self.wfile.write(bytes("Welcome " + user.username, 'utf-8'))

            except Exception:
                self.send_response(401)
                self.end_headers()


    server = HTTPServer(('', 8084), HandleRequest)
    print("Server is waiting...")
    server.serve_forever()
    server.server_close()

Check the audience
~~~~~~~~~~~~~~~~~~

Audience identifies the recipients that the token is intended for. Each resource
server MUST be identified by its audience name and the authorization process MUST
check that this audience exists in the token.

.. warning::
    By default, audience is not checked by the authentication process. It is
    the responsibility of the resource server to communicate its audience name
    in order to only accept token that has been generated for the this specific
    resource server.

To check the audience, add an ``options`` dictionary to the ``auth()`` or
``auth_from_http_headers()`` functions.

.. code:: python

    # Check that the provided token has a valid audience for api.pebble.solutions/v5/my-resource
    auth_token = auth("----my.valid.token----", options={
        'audience': "api.pebble.solutions/v5/my-resource"
    })

    # Check that token communicate through authorization header has a valid audience
    # for api.pebble.solutions/v5/my-resource
    auth_token = auth_from_http_headers(headers, options={
        'audience': "api.pebble.solutions/v5/my-resource"
    })
