import pytest

from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import SUfilter, SUimp2d, SUsort
from suspark.suspark_modules_factory import ModulesFactory, register_module_types


def test_pipeline_registry(suspark_context: SusparkContext, modules_factory: ModulesFactory) -> None:
    pipeline_repo = PiplineRepository(suspark_context=suspark_context, factory=modules_factory)

    name = "my pipe"
    item = pipeline_repo.add_pipeline(name)
    assert item.name == name

    item1 = pipeline_repo.get_pipeline(item.id)
    assert item1.name == name

    name = "another pipe"
    item2 = pipeline_repo.add_pipeline(name)
    assert item2.name == name

    ids = pipeline_repo.get_pipeline_ids()
    assert len(ids) == 2
    assert (item1.id, item1.name) in ids and (item2.id, item2.name) in ids
