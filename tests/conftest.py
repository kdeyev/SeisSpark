import pytest

from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory, register_module_types


@pytest.fixture(scope="session")
def suspark_context() -> SusparkContext:

    suspark_context = SusparkContext()
    return suspark_context


@pytest.fixture()
def modules_factory() -> ModulesFactory:

    factory = ModulesFactory()
    register_module_types(factory)
    return factory
