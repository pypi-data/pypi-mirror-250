from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.run import Run
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["parent_run_id"] = parent_run_id

    params["session_name"] = session_name

    params["root_node"] = root_node

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/runs/{id}".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Run]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Run.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Run]:
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
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Response[Run]:
    """
    Args:
        id (str):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Run]
    """

    kwargs = _get_kwargs(
        id=id,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Optional[Run]:
    """
    Args:
        id (str):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Run
    """

    return sync_detailed(
        id=id,
        client=client,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Response[Run]:
    """
    Args:
        id (str):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Run]
    """

    kwargs = _get_kwargs(
        id=id,
        parent_run_id=parent_run_id,
        session_name=session_name,
        root_node=root_node,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parent_run_id: Union[Unset, str] = UNSET,
    session_name: Union[Unset, str] = UNSET,
    root_node: Union[Unset, str] = UNSET,
) -> Optional[Run]:
    """
    Args:
        id (str):
        parent_run_id (Union[Unset, str]):
        session_name (Union[Unset, str]):
        root_node (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Run
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            parent_run_id=parent_run_id,
            session_name=session_name,
            root_node=root_node,
        )
    ).parsed
