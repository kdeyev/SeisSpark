from typing import List

import pydantic


def test_suspark_service_modules(suspark_service_client) -> None:
    response = suspark_service_client.get("/")
    assert response.status_code == 404

    response = suspark_service_client.get("/api/v1/modules")
    response.raise_for_status()
    module_types: List[str] = pydantic.parse_obj_as(List[str], response.json())
    assert module_types == ["SUfilter", "SUsort", "SUimp2d"]
