import unittest

from htmlnode import HTMLNode, LeafNode, NO_VALUE_ERROR

PARA = "Some paragraph"


class TestTextNode(unittest.TestCase):
    def test_html_node_initializes(self):
        html_node = HTMLNode("p", PARA, None, {"class": "myclass"})
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, PARA)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, {"class": "myclass"})

    def test_html_node_initializes_with_defaults(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_repr(self):
        html_node = HTMLNode("p", PARA, None, {"class": "myclass"})
        str_repr = """HTMLNode(\ntag: p\nvalue: Some paragraph...\nchildren: None\nprops:  class="myclass"\n)"""
        self.assertEqual(str(html_node), str_repr)

    def test_props_to_html(self):
        html_node = HTMLNode("p", PARA)
        html_node1 = HTMLNode("p", PARA, None, {"class": "myclass"})
        html_node2 = HTMLNode("p", PARA, None, {"id": "myid", "class": "myclass"})
        self.assertEqual(html_node.props_to_html(), "")
        self.assertEqual(html_node1.props_to_html(), ' class="myclass"')
        self.assertEqual(html_node2.props_to_html(), ' id="myid"  class="myclass"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_initializes(self):
        leaf_node = LeafNode("p", PARA)
        leaf_node1 = LeafNode("p", PARA, {"class": "myclass"})
        self.assertEqual(leaf_node.tag, "p")
        self.assertEqual(leaf_node.value, PARA)
        self.assertEqual(leaf_node1.tag, "p")
        self.assertEqual(leaf_node1.value, PARA)
        self.assertEqual(leaf_node1.props, {"class": "myclass"})

    def test_leaf_node_raises_with_no_value(self):
        with self.assertRaises(ValueError) as ve:
            LeafNode("p", None)
        self.assertEqual(ve.exception.args[0], NO_VALUE_ERROR)

    def test_to_html(self):
        leaf_node1 = LeafNode("p", PARA, {"class": "myclass"})
        self.assertEqual(leaf_node1.to_html(), f'<p class="myclass">{PARA}</p>')
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf_node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
