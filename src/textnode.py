import re
from enum import Enum

NO_URL_ERROR = (
    "No url provided. TextNode of link type needs a valid url to initialize",
)


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    CODE = "code"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        if self.text_type == TextType.LINK and not url:
            raise ValueError(NO_URL_ERROR)
        else:
            self.url = url

    def __eq__(self, node):
        try:
            return (
                self.text == node.text
                and self.text_type == node.text_type
                and self.url == node.url
            )
        except AttributeError:
            print(f"Node - '{node}' is not a known text node")
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


# Markdown Text helper methods


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_regex, text)
    return matches


def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_regex, text)
    return matches
