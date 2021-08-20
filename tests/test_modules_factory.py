import pytest

from suspark.suspark_module import SUfilter, SUimp2d
from suspark.suspark_modules_factory import ModulesFactory


def test_modules_factory() -> None:
    factory = ModulesFactory()
    # register_module_types(factory)
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUimp2d", SUimp2d)

    with pytest.raises(KeyError):
        factory.register_module_type("SUfilter", SUfilter)

    with pytest.raises(Exception):
        factory.register_module_type("SU filter", SUfilter)

    assert factory.get_module_types() == ["SUfilter", "SUimp2d"]
