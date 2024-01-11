from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.prompt import Prompt
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    body: Prompt,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["parent_id"] = parent_id

    params["root_id"] = root_id

    params["base_query"] = base_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": "/prompts/{id}".format(
            id=id,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Prompt]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Prompt.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Prompt]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Prompt,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Response[Prompt]:
    """
    Args:
        id (str):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):
        body (Prompt):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Prompt]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Prompt,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Optional[Prompt]:
    """
    Args:
        id (str):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):
        body (Prompt):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Prompt
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Prompt,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Response[Prompt]:
    """
    Args:
        id (str):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):
        body (Prompt):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Prompt]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Prompt,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Optional[Prompt]:
    """
    Args:
        id (str):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):
        body (Prompt):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Prompt
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            parent_id=parent_id,
            root_id=root_id,
            base_query=base_query,
        )
    ).parsed
