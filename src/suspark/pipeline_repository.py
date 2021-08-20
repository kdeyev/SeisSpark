import uuid
from typing import Dict, List, Tuple

from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory
from suspark.suspark_pipeline import Pipeline


class PiplineRepositoryItem:
    def __init__(self, id: str, name: str, pipeline: Pipeline) -> None:
        self._id = id
        self._name = name
        self._pipeline = pipeline

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class PiplineRepository:
    def __init__(self, suspark_context: SusparkContext, modules_factory: ModulesFactory) -> None:
        self._suspark_context = suspark_context
        self._modules_factory = modules_factory
        self._items: Dict[str, PiplineRepositoryItem] = {}

    def add_pipeline(self, name: str) -> PiplineRepositoryItem:
        id = str(uuid.uuid4())

        pipeline = Pipeline(suspark_context=self._suspark_context, modules_factory=self._modules_factory)
        item = PiplineRepositoryItem(id=id, name=name, pipeline=pipeline)
        self._items[id] = item

        return item

    def get_pipeline(self, id: str) -> PiplineRepositoryItem:
        return self._items[id]

    def get_pipeline_ids(self) -> List[Tuple[str, str]]:
        return [(item.id, item.name) for item in self._items.values()]
