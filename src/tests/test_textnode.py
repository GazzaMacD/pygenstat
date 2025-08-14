import unittest

from textnode import (
    TextNode,
    TextType,
    NO_URL_ERROR,
)

T = "This is a text node"
B = "This is a bold node"
I = "This is an italic node"
L = "This is a url node"
URL = "https://myurl.com"


class TestTextNode(unittest.TestCase):
    def test_text_node_initializes(self):
        text = TextNode(T, TextType.TEXT)
        self.assertEqual(text.text, T)
        self.assertEqual(text.text_type.value, "text")
        self.assertEqual(text.url, None)

    def test_bold_node_initializes(self):
        bold = TextNode(B, TextType.BOLD)
        self.assertEqual(bold.text, B)
        self.assertEqual(bold.text_type.value, "bold")
        self.assertEqual(bold.url, None)

    def test_italic_node_initializes(self):
        italic = TextNode(I, TextType.ITALIC)
        self.assertEqual(italic.text, I)
        self.assertEqual(italic.text_type.value, "italic")
        self.assertEqual(italic.url, None)

    def test_link_node_initializes(self):
        link = TextNode(L, TextType.LINK, URL)
        self.assertEqual(link.text, L)
        self.assertEqual(link.text_type.value, "link")
        self.assertEqual(link.url, URL)

    def test_link_node_raises_with_no_url_provided(self):
        with self.assertRaises(ValueError) as ve:
            TextNode(L, TextType.LINK)
        self.assertEqual(ve.exception.args[0], NO_URL_ERROR)

    def test_eq(self):
        node = TextNode(T, TextType.TEXT)
        node2 = TextNode(T, TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode(T, TextType.TEXT)
        node2 = TextNode(B, TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_representation(self):
        node = TextNode(L, TextType.LINK, URL)
        self.assertEqual(
            str(node), "TextNode(This is a url node, TextType.LINK, https://myurl.com)"
        )


if __name__ == "__main__":
    unittest.main()
