from typing import Dict, Type

from suspark.suspark_module import BaseModule


class ModulesFactory:
    def __init__(self) -> None:
        self._factory: Dict[str, Type[BaseModule]] = {}

    def create_module(self, module_type: str) -> BaseModule:
        return self._factory[module_type]()

    def register_module_type(self, module_type: str, module: Type[BaseModule]) -> None:
        self._factory[module_type] = module


def register_module_types(factory: ModulesFactory) -> None:
    from suspark.suspark_module import SUfilter, SUimp2d, SUsort

    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUsort", SUsort)
    factory.register_module_type("SUimp2d", SUimp2d)
