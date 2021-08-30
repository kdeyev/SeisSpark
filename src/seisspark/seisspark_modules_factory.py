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
from typing import Any, Dict, List, Type

from seisspark.seisspark_module import BaseModule


class ModulesFactory:
    def __init__(self) -> None:
        self._factory: Dict[str, Type[BaseModule]] = {}

    def create_module(self, module_type: str, id: str, name: str) -> BaseModule:
        return self._factory[module_type](id=id, name=name)

    def register_module_type(self, module_type: str, module: Type[BaseModule]) -> None:
        if " " in module_type:
            raise Exception("Module type should not incluse ' '")
        if module_type in self._factory:
            raise KeyError(f"Module type {module_type} has been registered alread")
        self._factory[module_type] = module

    def get_module_types(self) -> List[str]:
        return list(self._factory.keys())

    def get_module_params_json_schema(self, module_type: str) -> Dict[str, Any]:
        # FIXME: get module schema without building the module
        module = self._factory[module_type](id="dummy", name="dummy")
        return module.params_schema
