from dataclasses import dataclass


@dataclass
class AuthenticatedLicenceObject:
    app: str
    """Application for which the licence is generated (client_id or application name)"""

    issuer: str
    """Server that issued the authorization"""

    tenant_id: str
    """Customer id, client id... that will consume resources"""

    user: any
    """Instance of User class who own the licence"""
