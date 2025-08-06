from textnode import TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initializes an HTML Node

        Args:
            tag - (str) representing the HTML tag name (e.g. "p", "a", "h1", etc.)
            value - (str) representing the value of the HTML tag (e.g. the text inside a paragraph)
            children - (list) of HTMLNode objects representing the children of this node
            props - (dict) of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

        Attrs:
            self.tag - str or None
            self.value - str or None
            self.children - list or None
            self.props - dict or None

        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html needs implementation")

    def props_to_html(self):
        props = ""
        if not self.props:
            return props
        else:
            for k, v in self.props.items():
                props += f' {k}="{v}" '
            return props.rstrip()

    def __repr__(self) -> str:
        if self.value:
            return f"HTMLNode(\ntag: {self.tag}\nvalue: {self.value[:15] + '...'}\nchildren: {self.children}\nprops: {self.props_to_html()}\n)"
        else:
            return f"HTMLNode(\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props_to_html()}\n)"


NO_VALUE_ERROR = "init error: value is required"
NO_CHILDREN_ERROR = "init error: children is required"
NO_TAG_ERROR = "init error: tag is required"
UNKNOWN_TAG_ERROR = "ERROR: text_node_to_html_node requires a text node with a text_type of known value derived from TextType ennum."


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if not value:
            raise ValueError(NO_VALUE_ERROR)
        else:
            super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if not tag:
            raise ValueError(NO_TAG_ERROR)
        elif not children:
            raise ValueError(NO_CHILDREN_ERROR)
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError(NO_TAG_ERROR)
        if not self.children:
            raise ValueError(NO_CHILDREN_ERROR)
        props = self.props_to_html()
        start = f"<{self.tag}{props}>"
        end = f"</{self.tag}>"
        for child in self.children:
            start += child.to_html()
        return start + end


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", text_node.text, {"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception(UNKNOWN_TAG_ERROR)
