import unittest

from textnode import (
    TextNode,
    TextType,
    NO_URL_ERROR,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
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


class TestSplitNodes(unittest.TestCase):
    def test_bold_delimiter(self):
        text_node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold block")

    def test_raises_with_invalid_bold_delimiter(self):
        text_node = TextNode("This is text with a **bold block word", TextType.TEXT)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(
            ve.exception.args[0], "Invalid markdown, formatted section not closed"
        )

    def test_code_delimiter(self):
        text_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code block")

    def test_raises_with_invalid_code_delimiter(self):
        text_node = TextNode("This is text with a `bold block word", TextType.TEXT)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(
            ve.exception.args[0], "Invalid markdown, formatted section not closed"
        )

    def test_italic_delimiter(self):
        text_node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic block")

    def test_raises_with_invalid_italic_delimiter(self):
        text_node = TextNode("This is text with a _italic block word", TextType.TEXT)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(
            ve.exception.args[0], "Invalid markdown, formatted section not closed"
        )

    def test_nesting_delimiter(self):
        text_node = TextNode(
            "This is text with an _italic block_, a **bold block** and a `code block` in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter([text_node], "_", TextType.ITALIC),
                "`",
                TextType.CODE,
            ),
            "**",
            TextType.BOLD,
        )
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[1].text, "italic block")
        self.assertEqual(new_nodes[3].text, "bold block")
        self.assertEqual(new_nodes[5].text, "code block")


class TestRegexExtractionFunctions(unittest.TestCase):
    def test_extract_images(self):
        raw_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(raw_text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(matches, expected)

    def test_extract_links(self):
        raw_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(raw_text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(matches, expected)


class TestImageSplit(unittest.TestCase):
    def setUp(self):
        self.empty_str_node = TextNode("", TextType.TEXT)
        self.space_str_node = TextNode(" ", TextType.TEXT)
        self.img_only_str_node = TextNode(
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT
        )
        self.img_two_only_str_node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        self.img_two_str_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.img_two_link_str_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [google link](https://google.com) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

    def test_img_split_empty(self):
        expected = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_image([self.empty_str_node])
        self.assertEqual(new_nodes, expected)

    def test_img_split_space(self):
        expected = [TextNode(" ", TextType.TEXT)]
        new_nodes = split_nodes_image([self.space_str_node])
        self.assertEqual(new_nodes, expected)

    def test_img_only_split(self):
        expected = [
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        new_nodes = split_nodes_image([self.img_only_str_node])
        self.assertEqual(new_nodes, expected)

    def test_img_two_only_split(self):
        expected = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        new_nodes = split_nodes_image([self.img_two_only_str_node])
        self.assertEqual(new_nodes, expected)

    def test_img_two_split_images(self):
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        new_nodes = split_nodes_image([self.img_two_str_node])
        self.assertEqual(new_nodes, expected)

    def test_img_mixed_link_split_images(self):
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                " and a [google link](https://google.com) and another ", TextType.TEXT
            ),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        new_nodes = split_nodes_image([self.img_two_link_str_node])
        self.assertEqual(new_nodes, expected)


class TestLinkSplit(unittest.TestCase):
    def setUp(self):
        self.empty_str_node = TextNode("", TextType.TEXT)
        self.space_str_node = TextNode(" ", TextType.TEXT)
        self.link_only_str_node = TextNode(
            "[xlingual](https://xlingual.co.jp)", TextType.TEXT
        )
        self.link_two_only_str_node = TextNode(
            "[xlingual](https://xlingual.co.jp)[google](https://google.com)",
            TextType.TEXT,
        )
        self.link_two_str_node = TextNode(
            "This is text with an [xlingual](https://xlingual.co.jp) and another [google](https://google.com)",
            TextType.TEXT,
        )
        self.img_two_link_str_node = TextNode(
            "This is text with an [xlingual](https://xlingual.co.jp) and ![image](https://i.imgur.com/zjjcJKZ.png) and another [google](https://google.com)",
            TextType.TEXT,
        )

    def test_link_split_empty(self):
        expected = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_link([self.empty_str_node])
        self.assertEqual(new_nodes, expected)

    def test_link_split_space(self):
        expected = [TextNode(" ", TextType.TEXT)]
        new_nodes = split_nodes_link([self.space_str_node])
        self.assertEqual(new_nodes, expected)

    def test_link_only_split(self):
        expected = [TextNode("xlingual", TextType.LINK, "https://xlingual.co.jp")]
        new_nodes = split_nodes_link([self.link_only_str_node])
        self.assertEqual(new_nodes, expected)

    def test_link_two_only_split(self):
        expected = [
            TextNode("xlingual", TextType.LINK, "https://xlingual.co.jp"),
            TextNode("google", TextType.LINK, "https://google.com"),
        ]
        new_nodes = split_nodes_link([self.link_two_only_str_node])
        self.assertEqual(new_nodes, expected)

    def test_link_two_split(self):
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("xlingual", TextType.LINK, "https://xlingual.co.jp"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("google", TextType.LINK, "https://google.com"),
        ]
        new_nodes = split_nodes_link([self.link_two_str_node])
        self.assertEqual(new_nodes, expected)

    def test_link_two_image_mixed_split(self):
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("xlingual", TextType.LINK, "https://xlingual.co.jp"),
            TextNode(
                " and ![image](https://i.imgur.com/zjjcJKZ.png) and another ",
                TextType.TEXT,
            ),
            TextNode("google", TextType.LINK, "https://google.com"),
        ]
        new_nodes = split_nodes_link([self.img_two_link_str_node])
        self.assertEqual(new_nodes, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_all_nodes(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), len(expected))
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
