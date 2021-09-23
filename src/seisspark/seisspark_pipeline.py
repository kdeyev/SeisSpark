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
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Union

import pyspark

from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_module import BaseModule
from seisspark.seisspark_modules_factory import ModulesFactory
from su_rdd.kv_operations import GatherTuple


@dataclass
class GraphNodeConnection:
    id: str
    socket_index: int


class GraphNode:
    def __init__(self, module: BaseModule) -> None:
        self.module = module
        self.producers: List[Optional[GraphNodeConnection]] = [None for input_socket in self.module.input_sockets]
        self.consumers: List[Optional[GraphNodeConnection]] = [None for input_socket in self.module.output_sockets]

    def disconnect_producer(self, socket_index: int) -> None:
        self.producers[socket_index] = None

    def disconnect_consumer(self, socket_index: int) -> None:
        self.consumers[socket_index] = None

    # def connect_producer(self, my_index: int, ) -> None:
    #     self.producers[my_index] = None

    # def disconnect_consumer(self, index: int) -> None:
    #     self.consumers[index] = None


class Graph:
    def __init__(self) -> None:
        self._nodes: Dict[str, GraphNode] = {}

    def __getitem__(self, id: str) -> BaseModule:
        return self._nodes[id].module

    def __delitem__(self, id: str) -> None:
        node = self._nodes[id]
        for consumer in node.consumers:
            if consumer:
                consumer_node = self._nodes[consumer.id]
                consumer_node.disconnect_producer(consumer.socket_index)

        for producer in node.producers:
            if producer:
                producer_node = self._nodes[producer.id]
                producer_node.disconnect_consumer(producer.socket_index)

        del self._nodes[id]

    def __setitem__(self, id: str, v: BaseModule) -> None:
        self._nodes[id] = GraphNode(v)

    def connect_sockets(self, prodicer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> None:
        producer_node = self._nodes[prodicer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if prev_consumer:
            self._nodes[prev_consumer.id].producers[prev_consumer.socket_index] = None

        if prev_producer:
            self._nodes[prev_producer.id].consumers[prev_producer.socket_index] = None

        producer_node.consumers[producer_socket_index] = GraphNodeConnection(consumer_id, consumer_socket_index)
        consumer_node.producers[consumer_socket_index] = GraphNodeConnection(prodicer_id, producer_socket_index)

    def get_node(self, id: str) -> GraphNode:
        return self._nodes[id]

    def is_connected(self, prodicer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> bool:
        producer_node = self._nodes[prodicer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if not prev_consumer or not prev_producer:
            return False

        if prev_consumer.id != consumer_id or prev_consumer.socket_index != consumer_socket_index:
            return False

        if prev_producer.id != prodicer_id or prev_producer.socket_index != producer_socket_index:
            return False

        return True

    def disconnect_sockets(self, prodicer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> bool:
        if not self.is_connected(prodicer_id, producer_socket_index, consumer_id, consumer_socket_index):
            return False
        producer_node = self._nodes[prodicer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if prev_consumer:
            self._nodes[prev_consumer.id].producers[prev_consumer.socket_index] = None

        if prev_producer:
            self._nodes[prev_producer.id].consumers[prev_producer.socket_index] = None

        return True


class Pipeline:
    def __init__(self, seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
        self._modules_factory = modules_factory
        self._seisspark_context = seisspark_context
        self._modules = Graph()

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
