"""Minimal client for the official INEGI DENUE API.

The API places its token in the URL path. Never log the complete URL or include
it in exceptions. Tokens belong in DENUE_API_TOKEN, outside version control.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API_BASE = "https://www.inegi.org.mx/app/api/denue/v1/consulta"
USER_AGENT = "Rendify/0.1 (+https://github.com/donosty/rendify)"


class DenueApiError(RuntimeError):
    """Raised when DENUE cannot return a valid JSON list of establishments."""


@dataclass(frozen=True)
class DenueAreaActivityQuery:
    """Parameters for BuscarAreaAct; defaults to a small CDMX sample."""

    entity_code: str = "09"
    municipality_code: str = "0"
    locality_code: str = "0"
    ageb_code: str = "0"
    block_code: str = "0"
    sector_code: str = "0"
    subsector_code: str = "0"
    branch_code: str = "0"
    class_code: str = "0"
    establishment_name: str = "0"
    start_record: int = 1
    end_record: int = 15
    establishment_id: str = "0"

    def validate(self) -> None:
        _validate_geo_code(self.entity_code, 2, allow_all="00")
        _validate_geo_code(self.municipality_code, 3)
        _validate_geo_code(self.locality_code, 4)
        _validate_geo_code(self.ageb_code, 4)
        _validate_geo_code(self.block_code, 3)
        _validate_geo_code(self.sector_code, 2)
        _validate_geo_code(self.subsector_code, 3)
        _validate_geo_code(self.branch_code, 4)
        _validate_geo_code(self.class_code, 6)
        if not self.establishment_name:
            raise ValueError("establishment_name must not be empty; use '0' for all.")
        if self.start_record < 1:
            raise ValueError("start_record must be at least 1.")
        if self.end_record < self.start_record:
            raise ValueError("end_record must be greater than or equal to start_record.")
        if not self.establishment_id.isdigit():
            raise ValueError("establishment_id must be numeric; use '0' for all.")

    def to_manifest_dict(self) -> dict[str, Any]:
        """Return only safe query parameters, without credentials."""
        self.validate()
        return asdict(self)


def _validate_geo_code(value: str, expected_width: int, allow_all: str = "0") -> None:
    if value == allow_all:
        return
    if not value.isdigit() or len(value) != expected_width:
        raise ValueError(
            f"Expected a {expected_width}-digit code or '{allow_all}', got an invalid value."
        )


def build_buscar_area_act_url(query: DenueAreaActivityQuery, token: str) -> str:
    """Build the request URL. The caller must never log or persist this URL."""
    query.validate()
    if not token or not token.strip():
        raise ValueError("A non-empty DENUE API token is required.")

    segments = [
        query.entity_code,
        query.municipality_code,
        query.locality_code,
        query.ageb_code,
        query.block_code,
        query.sector_code,
        query.subsector_code,
        query.branch_code,
        query.class_code,
        query.establishment_name,
        str(query.start_record),
        str(query.end_record),
        query.establishment_id,
        token,
    ]
    encoded_segments = [quote(segment, safe="") for segment in segments]
    return f"{API_BASE}/BuscarAreaAct/{'/'.join(encoded_segments)}"


def fetch_page(
    query: DenueAreaActivityQuery,
    token: str,
    timeout: float = 30.0,
) -> tuple[bytes, list[dict[str, Any]], int, str]:
    """Fetch one page and return original bytes, parsed rows and HTTP metadata."""
    url = build_buscar_area_act_url(query, token)
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(response.status)
            content_type = response.headers.get("Content-Type", "")
            raw_body = response.read()
    except HTTPError as exc:
        raise DenueApiError(f"DENUE returned HTTP status {exc.code}.") from None
    except URLError:
        # Do not propagate urllib diagnostics: they may contain the tokenized URL.
        raise DenueApiError("DENUE request failed at transport layer.") from None
    except TimeoutError:
        raise DenueApiError("DENUE request timed out.") from None

    if status < 200 or status >= 300:
        raise DenueApiError(f"DENUE returned HTTP status {status}.")

    try:
        payload = json.loads(raw_body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise DenueApiError(
            "DENUE returned a successful HTTP response that was not valid UTF-8 JSON."
        ) from None

    if not isinstance(payload, list):
        raise DenueApiError("DENUE returned JSON, but the top-level value was not a list.")
    if any(not isinstance(row, dict) for row in payload):
        raise DenueApiError("DENUE returned a list containing a non-object record.")

    return raw_body, payload, status, content_type
