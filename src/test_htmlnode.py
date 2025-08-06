import unittest

from htmlnode import (
    NO_CHILDREN_ERROR,
    HTMLNode,
    LeafNode,
    NO_VALUE_ERROR,
    NO_TAG_ERROR,
    ParentNode,
    text_node_to_html_node,
)
from textnode import TextType, TextNode


PARA = "Some paragraph"


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode(
            "This is a grey image",
            TextType.IMAGE,
            "https://picsum.photos/200/300?grayscale",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a grey image")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://picsum.photos/200/300?grayscale",
                "alt": "This is a grey image",
            },
        )


class TestParentNode(unittest.TestCase):
    def test_parent_node_initilizes(self):
        p1 = LeafNode("p", (PARA + " 1"))
        p2 = LeafNode("p", (PARA + " 2"))
        div = ParentNode("div", [p1, p2], {"class": "mydiv"})
        self.assertEqual(div.tag, "div")
        self.assertEqual(div.children, [p1, p2])
        self.assertEqual(div.props, {"class": "mydiv"})

    def test_parent_node_raises_with_no_tag(self):
        p1 = LeafNode("p", (PARA + " 1"))
        p2 = LeafNode("p", (PARA + " 2"))
        with self.assertRaises(ValueError) as ve:
            ParentNode(None, [p1, p2], {"class": "mydiv"})
        self.assertEqual(ve.exception.args[0], NO_TAG_ERROR)

    def test_parent_node_raises_with_no_children(self):
        with self.assertRaises(ValueError) as ve:
            ParentNode("div", [], {"class": "mydiv"})
        self.assertEqual(ve.exception.args[0], NO_CHILDREN_ERROR)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("span", "child", {"id": "myid"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), '<div><span id="myid">child</span></div>'
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_props(self):
        p1 = LeafNode("p", (PARA + " 1"))
        p2 = LeafNode("p", (PARA + " 2"))
        div = ParentNode("div", [p1, p2], {"class": "mydiv"})
        result = div.to_html()
        expected = f'<div class="mydiv"><p>{PARA + " 1"}</p><p>{PARA + " 2"}</p></div>'
        self.assertEqual(result, expected)


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


class TestHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
