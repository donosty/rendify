from urllib.parse import quote

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

    """Build the URL for a DENUE BuscarAreaAct query."""

    # Validate the API token.
    if not token or not token.strip():
        raise ValueError("The DENUE API token cannot be empty.")

    # Validate the requested record range.
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