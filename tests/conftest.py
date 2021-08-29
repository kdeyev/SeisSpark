import pytest
from fastapi.testclient import TestClient

from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory
from suspark_modules.suspark_test_modules import register_test_modules
from suspark_service.suspark_service_app import create_suspark_service_app


@pytest.fixture(scope="session")
def suspark_context() -> SusparkContext:

    suspark_context = SusparkContext()
    return suspark_context


@pytest.fixture()
def modules_factory() -> ModulesFactory:
    factory = ModulesFactory()
    register_test_modules(factory)
    return factory


@pytest.fixture()
def suspark_service_client(
    modules_factory: ModulesFactory,
    suspark_context: SusparkContext,
) -> TestClient:

    pipeline_repository = PiplineRepository(suspark_context=suspark_context, modules_factory=modules_factory)

    app = create_suspark_service_app(modules_factory=modules_factory, pipeline_repository=pipeline_repository)

    client = TestClient(app)
    return client
