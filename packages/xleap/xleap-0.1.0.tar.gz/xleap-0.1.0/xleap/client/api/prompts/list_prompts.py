from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_prompts_response_200 import ListPromptsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["cursor"] = cursor

    params["parent_id"] = parent_id

    params["root_id"] = root_id

    params["base_query"] = base_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/prompts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListPromptsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListPromptsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListPromptsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Response[ListPromptsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPromptsResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Optional[ListPromptsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPromptsResponse200
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Response[ListPromptsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPromptsResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        parent_id=parent_id,
        root_id=root_id,
        base_query=base_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_id: Union[Unset, str] = UNSET,
    root_id: Union[Unset, str] = UNSET,
    base_query: Union[Unset, str] = UNSET,
) -> Optional[ListPromptsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        root_id (Union[Unset, str]):
        base_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPromptsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            parent_id=parent_id,
            root_id=root_id,
            base_query=base_query,
        )
    ).parsed
