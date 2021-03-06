from unittest.mock import patch

import pytest

from graph import Graph
from element import Edge, Geometry, Node


@pytest.mark.skip()
class TestGraph:

    @patch('xml.dom.minidom.parse', return_value=None)
    def setup(self, parse):
        self.path = 'test/path/file.graphml'
        self.graph = Graph(self.path)
        self.node_id = 'Test Node Id'
        self.edge_id = 'Test Edge Id'

    def test_output_path(self):
        assert self.graph.svg_path == self.path.replace('.graphml', '.svg')

        output_path = 'another/path/to/file.svg'
        g = Graph(self.path, output_path)
        assert g.svg_path == output_path

    def test_add_node(self):
        assert not self.graph.nodes
        self.graph.add_node(self.node_id)
        assert self.graph.nodes
        assert isinstance(self.graph.nodes[self.node_id], Node)

    def test_add_edge(self):
        assert not self.graph.edges
        geometry = Geometry(2, 3, 4, 23)
        n1 = Node('n1', 'key', 'text', 'rect', None, geometry, None, None)
        geometry.translate(2)
        n2 = Node('n2', 'key', 'text', 'rect', None, geometry, None, None)
        self.graph.nodes['n1'] = n1
        self.graph.nodes['n2'] = n2

        self.graph.add_edge(self.edge_id, source=n1.id, target=n2.id)
        assert self.graph.edges
        assert isinstance(self.graph.edges[self.edge_id], Edge)
        assert self.graph.edges[self.edge_id].source == n1
        assert self.graph.edges[self.edge_id].target == n2

    def test_get_attrs(self):
        node = self.graph.xml.getElementsByTagName('node')[0]
        attribute = 'data'
        assert node.getElementsByTagName(attribute)
        assert self.graph.get_attrs(node, attribute)

        attribute = 'not in node'
        assert not node.getElementsByTagName(attribute)
        assert not self.graph.get_attrs(node, attribute)

    def test_node_text(self):
        pass
