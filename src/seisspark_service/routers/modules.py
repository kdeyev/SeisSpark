# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from typing import Any, Dict, List

from fastapi import Path

from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_service.inferring_router import InferringRouter


def init_router(modules_factory: ModulesFactory) -> InferringRouter:
    router = InferringRouter()

    @router.get("/modules", tags=["modules"])
    def get_modules() -> List[str]:
        return modules_factory.get_module_types()

    @router.get("/modules/{module_type}", tags=["modules"])
    def get_module_schema(module_type: str = Path(...)) -> Dict[str, Any]:
        return modules_factory.get_module_params_json_schema(module_type)

    return router
