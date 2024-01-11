from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_runs_response_200 import ListRunsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["cursor"] = cursor

    params["parent_run_id"] = parent_run_id

    params["session_name"] = session_name

    params["root_node"] = root_node

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/runs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListRunsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListRunsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListRunsResponse200]:
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
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Response[ListRunsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunsResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Optional[ListRunsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunsResponse200
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Response[ListRunsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunsResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Optional[ListRunsResponse200]:
    """
    Args:
        cursor (Union[Unset, str]):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            parent_run_id=parent_run_id,
            session_name=session_name,
            root_node=root_node,
        )
    ).parsed
