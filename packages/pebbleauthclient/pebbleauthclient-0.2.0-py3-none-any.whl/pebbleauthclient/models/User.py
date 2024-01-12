import re
from typing import Sequence
from pebbleauthclient.datatypes import UserObject


class User(UserObject):
    """
    This object represent an authenticated user.

    :param user: UserObject
    """
    def __init__(self, user: UserObject):

        self.username: str = user.username
        """User name (should be an email)"""

        self.display_name: str = user.display_name
        """Name to be displayed (free 255 chars). Nullable"""

        self.level: int = user.level
        """User level from 1 to 6"""

        self.roles: Sequence[str] = user.roles
        """Roles granted to the user"""

        self.scopes: Sequence[str] = user.scopes
        """List of authorized scope for the user"""

    def has_role(self, role: str) -> bool:
        """
        Check if the user has the argument specified role.

        :param role: str
        :return: bool
        """
        if self.roles:
            return role in self.roles
        return False

    def has_scopes(self, scopes: Sequence[str], policy: str = None) -> bool:
        """
        Check if the user is granted on the provided scopes.

        :param scopes: Sequence[str]    A list of scopes
        :param policy: str              ONE = Return true if one scope is valid, ALL = Return true if all scope are
                                        valid. Default is ONE

        :return:
        """

        policy = policy if policy else 'ONE'

        if not self.scopes or not len(scopes):
            return False

        count = 0

        for input_scope in scopes:

            # This line gets the unfiltered action: api:action.filter become api: action
            unfiltered_scope = re.sub('\.[\w\*]+$', "", input_scope)

            # This line gets the action name only
            action = re.sub('^\w+:(\w+)\.?[\w\*]*', r"\1", input_scope)

            for user_scope in self.scopes:

                # If the user scope use a joker ( * ), it is replaced with the current action (joker means any action).
                if re.match(':\*', user_scope):
                    user_scope = re.sub(':\*', ":"+action, user_scope)

                if input_scope == user_scope or unfiltered_scope == user_scope:
                    if policy.upper() == 'ONE':
                        return True

                    count +=1

            return count >= len(scopes)