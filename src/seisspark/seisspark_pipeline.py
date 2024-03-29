# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import collections
import uuid
from typing import Dict, Iterator, List, Optional, Union

import pyspark

from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_module import BaseModule
from seisspark.seisspark_modules_factory import ModulesFactory
from su_rdd.kv_operations import GatherTuple


class BaseModuleList(collections.MutableSequence):
    def __init__(self) -> None:
        self._l: List[BaseModule] = []
        self._d: Dict[str, BaseModule] = {}

    def __len__(self) -> int:
        return len(self._l)

    def __getitem__(self, i: Union[str, int]) -> BaseModule:  # type: ignore
        if type(i) is int:
            return self._l[i]
        elif type(i) is str:
            return self._d[i]
        else:
            raise Exception(f"Wrong key type {type(i)}")

    def __delitem__(self, i: Union[str, int]) -> None:  # type: ignore
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

    def __setitem__(self, i: int, v: BaseModule) -> None:  # type: ignore
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
    def __init__(self, seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
        self._modules_factory = modules_factory
        self._seisspark_context = seisspark_context
        self._modules = BaseModuleList()

    def modules(self) -> Iterator[BaseModule]:
        yield from self._modules

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
        rdd: Optional["pyspark.RDD[GatherTuple]"] = None
        for module in self._modules:
            module.init_rdd(self._seisspark_context, rdd)
            rdd = module.rdd
