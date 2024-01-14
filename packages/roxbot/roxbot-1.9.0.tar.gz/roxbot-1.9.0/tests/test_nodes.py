from roxbot.nodes.base import Node


class DummyNode(Node):
    async def main(self):
        pass


def test_node_creation():
    node = DummyNode("TestNode")
    assert node.name == "TestNode"

    # repr
    assert repr(node) == "<DummyNode TestNode>"
