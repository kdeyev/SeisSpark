import collections
from contextlib import contextmanager
from typing import Dict, Generator, List, Optional, Union

import pyspark

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
            j = any(self._l[j].id == i for j in range(len(self._l)))
            return self.l[j]
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def __setitem__(self, i: int, v: BaseModule) -> None:
        if type(i) is int:
            self._l[i] = v
            self._d[v.id] = v
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def insert(self, i: int, v: BaseModule):
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
    def __init__(self, spark_ctxt: pyspark.SparkContext, factory: ModulesFactory) -> None:
        self._factory = factory
        self._spark_ctxt = spark_ctxt
        self._modules = BaseModuleList()

    def add_module(self, module_type: str, prev_module_id: Optional[str] = None) -> str:
        index: Optional[int] = None
        if prev_module_id:
            index = self._modules.find_index(prev_module_id) + 1

        module = self._factory.create_module(module_type)
        if index is not None:
            self._modules.insert(index, module)
        else:
            self._modules.append(module)
        self._init_rdd()
        return module.id

    @contextmanager
    def get_module_r(self, module_id: str) -> Generator[BaseModule, None, None]:
        yield self._modules[module_id]

    @contextmanager
    def get_module_w(self, module_id: str) -> Generator[BaseModule, None, None]:
        yield self._modules[module_id]
        self._init_rdd()

    def delete_module(self, module_id: str) -> None:
        del self._modules[module_id]

    def _init_rdd(self) -> None:
        rdd: Optional[pyspark.RDD] = None
        for module in self._modules:
            module.init_rdd(self._spark_ctxt, rdd)
            rdd = module.rdd
