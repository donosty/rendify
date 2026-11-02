"""HTTP client helpers for querying the INEGI DENUE API."""

import json

from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from rendify.denue.exceptions import DenueAPIError

BASE_URL = "https://www.inegi.org.mx/app/api/denue/v1/consulta"

def build_buscar_area_act_url(
    entity: str,
    municipality: str,
    locality: str,
    ageb: str,
    block: str,
    sector: str,
    subsector: str,
    branch: str,
    class_code: str,
    establishment_name: str,
    record_start: int,
    record_end: int,
    establishment_id: str,
    token: str,
) -> str:
    """Build a validated, URL-encoded DENUE ``BuscarAreaAct`` endpoint."""

    # Reject requests that cannot be authenticated.
    if not token or not token.strip():
        raise ValueError("The DENUE API token cannot be empty.")

    # DENUE uses a one-based inclusive range for returned records.
    if record_start < 1:
        raise ValueError("record_start must be greater than or equal to 1.")

    if record_end < record_start:
        raise ValueError("record_end must be greater than or equal to record_start.")
    
    parameters = [
        entity,
        municipality,
        locality,
        ageb,
        block,
        sector,
        subsector,
        branch,
        class_code,
        establishment_name,
        record_start,
        record_end,
        establishment_id,
        token,
    ]

    encoded_parameters = [
        quote(str(parameter), safe="") for parameter in parameters
    ]

    return (
        f"{BASE_URL}/BuscarAreaAct/"
        f"{'/'.join(encoded_parameters)}"
    )


def fetch_buscar_area_act(
    *,
    entity: str,
    municipality: str,
    locality: str,
    ageb: str,
    block: str,
    sector: str,
    subsector: str,
    branch: str,
    class_code: str,
    establishment_name: str,
    record_start: int,
    record_end: int,
    establishment_id: str,
    token: str,
    timeout: float = 30.0,
) -> list[dict[str, Any]]:
    """Request an area/activity sample and return its JSON object records."""

    url = build_buscar_area_act_url(
        entity=entity,
        municipality=municipality,
        locality=locality,
        ageb=ageb,
        block=block,
        sector=sector,
        subsector=subsector,
        branch=branch,
        class_code=class_code,
        establishment_name=establishment_name,
        record_start=record_start,
        record_end=record_end,
        establishment_id=establishment_id,
        token=token,
    )

    request = Request(url, headers={"Accept": "application/json"})

    try:
        # Keep network failures behind one domain-specific exception.
        with urlopen(request, timeout=timeout) as response:
            response_body = response.read()
    except HTTPError as error:
        raise DenueAPIError(
            f"DENUE returned HTTP status {error.code}"
        ) from None
    except TimeoutError:
        raise DenueAPIError(
            "The request to DENUE timed out"
        ) from None
    except URLError:
        raise DenueAPIError(
            "Could not establish a connection with DENUE"
        ) from None

    try:
        # ``utf-8-sig`` also accepts regular UTF-8 while removing a BOM.
        records = json.loads(response_body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DenueAPIError(
            "DENUE returned a response that is not valid UTF-8 JSON"
        ) from error

    # Enforce the response shape promised by the return type.
    if not isinstance(records, list):
        raise DenueAPIError(
            "DENUE response must be a JSON list"
        )

    if not all(isinstance(record, dict) for record in records):
        raise DenueAPIError(
            "DENUE response contains elements that are not JSON objects"
        )

    return records