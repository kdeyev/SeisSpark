import pytest

from suspark.suspark_module import SUfilter, SUimp2d, SUsort
from suspark.suspark_modules_factory import ModulesFactory, register_module_types


def test_modules_factory() -> None:
    factory = ModulesFactory()
    # register_module_types(factory)
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUimp2d", SUimp2d)

    with pytest.raises(KeyError):
        factory.register_module_type("SUfilter", SUfilter)

    assert factory.get_module_types() == ["SUfilter", "SUimp2d"]
