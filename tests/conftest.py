import pytest
from fastapi.testclient import TestClient

from seisspark.pipeline_repository import PiplineRepository
from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_modules.seisspark_test_modules import register_test_modules
from seisspark_service.seisspark_service_app import create_seisspark_service_app


@pytest.fixture(scope="session")
def seisspark_context() -> SeisSparkContext:

    seisspark_context = SeisSparkContext()
    return seisspark_context


@pytest.fixture()
def modules_factory() -> ModulesFactory:
    factory = ModulesFactory()
    register_test_modules(factory)
    return factory


@pytest.fixture()
def seisspark_service_client(
    modules_factory: ModulesFactory,
    seisspark_context: SeisSparkContext,
) -> TestClient:

    pipeline_repository = PiplineRepository(seisspark_context=seisspark_context, modules_factory=modules_factory)

    app = create_seisspark_service_app(modules_factory=modules_factory, pipeline_repository=pipeline_repository)

    client = TestClient(app)
    return client
