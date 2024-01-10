"""get_runs SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.schema.generic_model import DeserializableModel

__all__ = ['get_users']

QUERY_FUNCTION = 'getAllUsers'
VARIABLE_DATA_NAME = 'getAllUsersData'
QUERY = f"""
query GetAllUsers(${VARIABLE_DATA_NAME}: GetAllUsersInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
        id
        name
        email
        organizations {{
            id,
            name
        }}
    }}
}}"""


@dataclass
class Organization(DeserializableModel):
    id: str
    name: str

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Organization:
        return cls(id=response['id'], name=response['name'])


@dataclass
class User(DeserializableModel):
    id: str
    name: str
    email: str
    organizations: List[Organization] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> User:
        organizations = [Organization.from_mapi_response(o) for o in response['organizations']]
        return cls(
            id=response['id'],
            name=response['name'],
            email=response['email'],
            organizations=organizations,
        )


@overload
def get_users(
    users: Optional[Union[List[str], List[User]]] = None,
    *,
    user_emails: Optional[List[str]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[User]:
    ...


@overload
def get_users(
    users: Optional[Union[List[str], List[User]]] = None,
    *,
    user_emails: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[User]]:
    ...


def get_users(
    users: Optional[Union[List[str], List[User]]] = None,
    *,
    user_emails: Optional[List[str]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """List users in the MosaicML platform

    Arguments:
        user_ids: List of user ids to get. This can be a list of ID strings or :type User: objects.
        user_emails: List of user emails to get.
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_users` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    filters = {}
    if users:
        filters['id'] = {'in': [u.id if isinstance(u, User) else u for u in users]}
    if user_emails is not None:
        filters['email'] = {'in': user_emails}

    variables = {VARIABLE_DATA_NAME: {'filters': filters,}}

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=User,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
