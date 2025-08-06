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
            print(f"ERROR: node - '{node}' is not a known text node")
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
