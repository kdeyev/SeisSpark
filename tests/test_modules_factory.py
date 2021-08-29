import pytest

from suspark.suspark_modules_factory import ModulesFactory
from suspark_modules.sufilter import SUfilter
from suspark_modules.suimp2d import SUimp2d


def test_modules_factory() -> None:
    factory = ModulesFactory()
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUimp2d", SUimp2d)

    with pytest.raises(KeyError):
        factory.register_module_type("SUfilter", SUfilter)

    with pytest.raises(Exception):
        factory.register_module_type("SU filter", SUfilter)

    assert factory.get_module_types() == ["SUfilter", "SUimp2d"]
