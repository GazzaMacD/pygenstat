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
            for k, v in self.props.values():
                props += f' {k}="{v}" '
            return props
