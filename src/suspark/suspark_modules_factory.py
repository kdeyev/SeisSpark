from typing import Any, Dict, List, Type

from suspark.suspark_module import BaseModule


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

    def get_module_params_json_schema(self, module_type: str) -> Any:
        # FIXME: get module schema without building the module
        module = self._factory[module_type](id="dummy", name="dummy")
        return module.params_schema
