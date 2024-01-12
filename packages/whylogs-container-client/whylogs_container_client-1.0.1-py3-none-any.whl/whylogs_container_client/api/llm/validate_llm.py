from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.llm_validate_request import LLMValidateRequest
from ...models.validation_report import ValidationReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    json_body: LLMValidateRequest,
    log: Union[Unset, bool] = True,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["log"] = log

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/validate/llm",
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ValidationReport]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ValidationReport.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ValidationReport.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ValidationReport]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: LLMValidateRequest,
    log: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ValidationReport]]:
    r"""Validate a single prompt/response pair

     This endpoint can be used to synchronously get validation results from a single input
    prompt/response. It automatically performs whylogs profiling and sends profiles to
    whylabs in the background, just like  the /log endpoint.

    Args:
        log (bool, optional): Determines if logging to WhyLabs is enabled for the validate request.
    Defaults to True.


    ## Sample curl request:

    ```bash
    curl -X 'POST'     -H \"X-API-Key: <password>\"     -H \"Content-Type: application/octet-stream\"
    'http://localhost:8000/validate/llm'     --data-raw '{
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }'
    ```

    ## Sample Python request:
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/validate/llm'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        log (Union[Unset, bool]):  Default: True.
        json_body (LLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ValidationReport]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        log=log,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: LLMValidateRequest,
    log: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ValidationReport]]:
    r"""Validate a single prompt/response pair

     This endpoint can be used to synchronously get validation results from a single input
    prompt/response. It automatically performs whylogs profiling and sends profiles to
    whylabs in the background, just like  the /log endpoint.

    Args:
        log (bool, optional): Determines if logging to WhyLabs is enabled for the validate request.
    Defaults to True.


    ## Sample curl request:

    ```bash
    curl -X 'POST'     -H \"X-API-Key: <password>\"     -H \"Content-Type: application/octet-stream\"
    'http://localhost:8000/validate/llm'     --data-raw '{
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }'
    ```

    ## Sample Python request:
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/validate/llm'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        log (Union[Unset, bool]):  Default: True.
        json_body (LLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ValidationReport]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        log=log,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: LLMValidateRequest,
    log: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ValidationReport]]:
    r"""Validate a single prompt/response pair

     This endpoint can be used to synchronously get validation results from a single input
    prompt/response. It automatically performs whylogs profiling and sends profiles to
    whylabs in the background, just like  the /log endpoint.

    Args:
        log (bool, optional): Determines if logging to WhyLabs is enabled for the validate request.
    Defaults to True.


    ## Sample curl request:

    ```bash
    curl -X 'POST'     -H \"X-API-Key: <password>\"     -H \"Content-Type: application/octet-stream\"
    'http://localhost:8000/validate/llm'     --data-raw '{
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }'
    ```

    ## Sample Python request:
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/validate/llm'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        log (Union[Unset, bool]):  Default: True.
        json_body (LLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ValidationReport]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        log=log,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: LLMValidateRequest,
    log: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ValidationReport]]:
    r"""Validate a single prompt/response pair

     This endpoint can be used to synchronously get validation results from a single input
    prompt/response. It automatically performs whylogs profiling and sends profiles to
    whylabs in the background, just like  the /log endpoint.

    Args:
        log (bool, optional): Determines if logging to WhyLabs is enabled for the validate request.
    Defaults to True.


    ## Sample curl request:

    ```bash
    curl -X 'POST'     -H \"X-API-Key: <password>\"     -H \"Content-Type: application/octet-stream\"
    'http://localhost:8000/validate/llm'     --data-raw '{
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }'
    ```

    ## Sample Python request:
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/validate/llm'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"prompt\": \"This is a test prompt\",
        \"response\": \"This is a test response\"
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        log (Union[Unset, bool]):  Default: True.
        json_body (LLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ValidationReport]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            log=log,
        )
    ).parsed
