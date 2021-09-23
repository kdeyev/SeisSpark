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
import pydantic
import pytest

from seisspark.seisspark_module import BaseModule, SocketDescription
from seisspark.seisspark_pipeline import Graph


class ImpotSegyParams(pydantic.BaseModel):
    pass


class Dummy2Input2Output(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(
            id=id,
            name=name,
            input_sockets=[SocketDescription("input1"), SocketDescription("input2")],
            output_sockets=[SocketDescription("output1"), SocketDescription("output2")],
        )


def test_pipiline_build() -> None:
    graph = Graph()
    graph["1"] = Dummy2Input2Output("1", "1")
    assert graph["1"].name == "1"

    with pytest.raises(KeyError):
        graph["2"]

    graph["2"] = Dummy2Input2Output("2", "2")
    assert graph["2"].name == "2"

    del graph["2"]
    with pytest.raises(KeyError):
        graph["2"]


def test_pipiline_graph_connect() -> None:
    graph = Graph()
    graph["1"] = Dummy2Input2Output("1", "1")
    graph["2"] = Dummy2Input2Output("2", "2")
    graph.connect_sockets("1", 0, "2", 0)
    assert graph.is_connected("1", 0, "2", 0)
    assert not graph.is_connected("1", 1, "2", 0)
    graph.disconnect_sockets("1", 0, "2", 0)
    assert not graph.is_connected("1", 0, "2", 0)

    del graph["2"]
    node1 = graph.get_node("1")
    assert node1.consumers == [None, None]


def test_pipiline_graph_traverse() -> None:
    graph = Graph()
    graph["1"] = Dummy2Input2Output("1", "1")
    graph["2"] = Dummy2Input2Output("2", "2")
    graph.connect_sockets("1", 0, "2", 0)

    producers = graph.get_producers()
    assert len(producers) == 1 and producers[0] == "1"

    consumers = graph.get_consumers()
    assert len(consumers) == 1 and consumers[0] == "2"

    topo_sort = list(graph.topology_sort())
    assert topo_sort == ["1", "2"]


def test_pipiline_graph_cycle() -> None:
    graph = Graph()
    graph["1"] = Dummy2Input2Output("1", "1")
    graph["2"] = Dummy2Input2Output("2", "2")
    graph.connect_sockets("1", 0, "2", 0)
    with pytest.raises(Exception):
        graph.connect_sockets("2", 0, "1", 0)
