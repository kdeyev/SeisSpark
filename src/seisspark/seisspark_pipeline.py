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
import uuid
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional

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

    def is_producer(self) -> bool:
        return all(producer is None for producer in self.producers)

    def is_consumer(self) -> bool:
        return all(consumer is None for consumer in self.consumers)

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

    def modules(self) -> Generator[BaseModule, None, None]:
        for node in self._nodes.values():
            yield node.module

    def topology_sort(self) -> Generator[str, None, None]:
        producers: List[str] = self.get_producers()
        already_travsersed: List[str] = []
        while producers:
            producer_id = producers.pop(0)
            yield producer_id

            already_travsersed.append(producer_id)

            producer_node = self.get_node(producer_id)
            for consumer in producer_node.consumers:
                if consumer and consumer.id not in already_travsersed:
                    producers.append(consumer.id)

    def connect_sockets(self, producer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> None:
        producer_node = self._nodes[producer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if prev_consumer:
            self._nodes[prev_consumer.id].producers[prev_consumer.socket_index] = None

        if prev_producer:
            self._nodes[prev_producer.id].consumers[prev_producer.socket_index] = None

        producer_node.consumers[producer_socket_index] = GraphNodeConnection(consumer_id, consumer_socket_index)
        consumer_node.producers[consumer_socket_index] = GraphNodeConnection(producer_id, producer_socket_index)

    def get_node(self, id: str) -> GraphNode:
        return self._nodes[id]

    def is_connected(self, producer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> bool:
        producer_node = self._nodes[producer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if not prev_consumer or not prev_producer:
            return False

        if prev_consumer.id != consumer_id or prev_consumer.socket_index != consumer_socket_index:
            return False

        if prev_producer.id != producer_id or prev_producer.socket_index != producer_socket_index:
            return False

        return True

    def disconnect_sockets(self, producer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> bool:
        if not self.is_connected(producer_id, producer_socket_index, consumer_id, consumer_socket_index):
            return False
        producer_node = self._nodes[producer_id]
        prev_consumer = producer_node.consumers[producer_socket_index]
        consumer_node = self._nodes[consumer_id]
        prev_producer = consumer_node.producers[consumer_socket_index]

        if prev_consumer:
            self._nodes[prev_consumer.id].producers[prev_consumer.socket_index] = None

        if prev_producer:
            self._nodes[prev_producer.id].consumers[prev_producer.socket_index] = None

        return True

    def get_producers(self) -> List[str]:
        producers: List[str] = []
        for id, node in self._nodes.items():
            if node.is_producer():
                producers.append(id)
        return producers

    def get_consumers(self) -> List[str]:
        consumers: List[str] = []
        for id, node in self._nodes.items():
            if node.is_consumer():
                consumers.append(id)
        return consumers


class Pipeline:
    def __init__(self, seisspark_context: SeisSparkContext, modules_factory: ModulesFactory) -> None:
        self._modules_factory = modules_factory
        self._seisspark_context = seisspark_context
        self._graph = Graph()
        self._module_rdds: Dict[str, List[Optional["pyspark.RDD[GatherTuple]"]]] = {}
        self._valid = False
        self._error_message = ""

    # def modules(self) -> Iterator[BaseModule]:
    #     yield from self._graph

    def add_module(self, module_type: str, name: Optional[str] = None, producers: Optional[List[GraphNodeConnection]] = None) -> BaseModule:
        id: str = str(uuid.uuid4())

        module = self._modules_factory.create_module(module_type, id, name if name else module_type)
        self._graph[id] = module
        if producers is not None:
            try:
                if len(producers) != len(module.input_sockets):
                    raise Exception(f"{len(producers)} producers was provided, but {len(module.input_sockets)} are required")
                for consumer_socket_index in range(len(module.input_sockets)):
                    producer = producers[consumer_socket_index]
                    self._graph.connect_sockets(producer.id, producer.socket_index, id, consumer_socket_index)
            except Exception as e:
                del self._graph[id]
                raise e
        self._init_rdd()
        return module

    def connect_modules(self, producer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> None:
        self._graph.connect_sockets(producer_id, producer_socket_index, consumer_id, consumer_socket_index)

    def disconnect_modules(self, producer_id: str, producer_socket_index: int, consumer_id: str, consumer_socket_index: int) -> None:
        self._graph.disconnect_sockets(producer_id, producer_socket_index, consumer_id, consumer_socket_index)

    def get_module(self, module_id: str) -> BaseModule:
        return self._graph[module_id]

    def delete_module(self, module_id: str) -> None:
        del self._graph[module_id]
        self._init_rdd()

    def _init_rdd(self) -> None:
        try:
            self._valid = True
            self._error_message = ""

            module_rdds: Dict[str, List[Optional["pyspark.RDD[GatherTuple]"]]] = {}
            for module_id in self._graph.topology_sort():
                node = self._graph.get_node(module_id)
                input_rdds: List[Optional["pyspark.RDD[GatherTuple]"]] = []
                for producer in node.producers:
                    produced_rdd: Optional["pyspark.RDD[GatherTuple]"] = None
                    if producer and producer.id in module_rdds:
                        produced_rdd = module_rdds[producer.id][producer.socket_index]
                    input_rdds.append(produced_rdd)

                output_rdds = node.module.init_rdd(self._seisspark_context, input_rdds)
                if len(output_rdds) != len(node.consumers):
                    raise Exception(f"Module {module_id} produced {len(output_rdds)} RDDs when it has {len(node.consumers)} output sockets")
                module_rdds[module_id] = output_rdds

            self._module_rdds = module_rdds
        except Exception as e:
            self._module_rdds = {}
            self._valid = False
            self._error_message = str(e)
