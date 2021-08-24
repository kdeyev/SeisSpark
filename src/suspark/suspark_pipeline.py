import collections
import uuid
from contextlib import contextmanager
from typing import Dict, Generator, Iterator, List, Optional, Union

import pyspark
from pydantic.main import BaseModel

from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule
from suspark.suspark_modules_factory import ModulesFactory


class BaseModuleList(collections.MutableSequence):
    def __init__(self):
        self._l: List[BaseModule] = []
        self._d: Dict[str, BaseModule] = {}

    def __len__(self) -> int:
        return len(self._l)

    def __getitem__(self, i: Union[str, int]) -> BaseModule:
        if type(i) is int:
            return self._l[i]
        elif type(i) is str:
            return self._d[i]
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def __delitem__(self, i: Union[str, int]) -> None:
        if type(i) is int:
            item: BaseModule = self._l[i]
            del self._d[item.id]
            del self._l[i]
        elif type(i) is str:
            item = self._d[i]
            j = next(j for j in range(len(self._l)) if self._l[j].id == i)
            del self._d[i]
            del self._l[j]
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def __setitem__(self, i: int, v: BaseModule) -> None:
        if type(i) is int:
            self._l[i] = v
            self._d[v.id] = v
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def insert(self, i: int, v: BaseModule) -> None:
        if type(i) is int:
            self._l.insert(i, v)
            self._d[v.id] = v
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def find_index(self, i: str) -> int:
        if type(i) is str:
            j = next(j for j in range(len(self._l)) if self._l[j].id == i)
            if j is None:
                raise ValueError()
            return j
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def __str__(self) -> str:
        return str(self._l)


class Pipeline:
    def __init__(self, suspark_context: SusparkContext, modules_factory: ModulesFactory) -> None:
        self._modules_factory = modules_factory
        self._suspark_context = suspark_context
        self._modules = BaseModuleList()

    def modules(self) -> Iterator[BaseModule]:
        for module in self._modules:
            yield module

    def add_module(self, module_type: str, name: Optional[str] = None, prev_module_id: Optional[str] = None) -> BaseModule:
        index: Optional[int] = None
        if prev_module_id:
            index = self._modules.find_index(prev_module_id) + 1

        id: str = str(uuid.uuid4())

        module = self._modules_factory.create_module(module_type, id, name if name else module_type)
        if index is not None:
            self._modules.insert(index, module)
        else:
            self._modules.append(module)
        self._init_rdd()
        return module

    def move_module(self, module_id: str, prev_module_id: Optional[str] = None) -> None:
        if module_id == prev_module_id:
            raise Exception("module_id == prev_module_id")
        module = self._modules[module_id]
        del self._modules[module_id]
        index = 0
        if prev_module_id:
            index = self._modules.find_index(prev_module_id) + 1

        self._modules.insert(index, module)
        self._init_rdd()

    def get_module(self, module_id: str) -> BaseModule:
        return self._modules[module_id]

    def delete_module(self, module_id: str) -> None:
        del self._modules[module_id]
        self._init_rdd()

    def _init_rdd(self) -> None:
        rdd: Optional[pyspark.RDD] = None
        for module in self._modules:
            module.init_rdd(self._suspark_context, rdd)
            rdd = module.rdd
