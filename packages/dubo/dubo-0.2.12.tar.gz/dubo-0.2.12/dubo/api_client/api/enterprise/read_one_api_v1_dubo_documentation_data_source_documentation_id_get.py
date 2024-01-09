from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_source_document import DataSourceDocument
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    data_source_documentation_id: str,
) -> Dict[str, Any]:
    return {
        "method": "get",
        "url": "/api/v1/dubo/documentation/{data_source_documentation_id}".format(
            data_source_documentation_id=data_source_documentation_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DataSourceDocument, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DataSourceDocument.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DataSourceDocument, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    data_source_documentation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DataSourceDocument, HTTPValidationError]]:
    """Read One

    Args:
        data_source_documentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataSourceDocument, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        data_source_documentation_id=data_source_documentation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    data_source_documentation_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DataSourceDocument, HTTPValidationError]]:
    """Read One

    Args:
        data_source_documentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DataSourceDocument, HTTPValidationError]
    """

    return sync_detailed(
        data_source_documentation_id=data_source_documentation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    data_source_documentation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DataSourceDocument, HTTPValidationError]]:
    """Read One

    Args:
        data_source_documentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataSourceDocument, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        data_source_documentation_id=data_source_documentation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    data_source_documentation_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DataSourceDocument, HTTPValidationError]]:
    """Read One

    Args:
        data_source_documentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DataSourceDocument, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            data_source_documentation_id=data_source_documentation_id,
            client=client,
        )
    ).parsed
