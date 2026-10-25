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