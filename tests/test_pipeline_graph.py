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
