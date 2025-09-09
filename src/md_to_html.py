from text_functions import markdown_to_blocks, text_to_text_nodes
from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from blocks import BlockType, block_to_blocktype, determine_heading_number


def markdown_to_html_node(markdown):
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            heading_node = md_to_heading_html_node(block)
            nodes.append(heading_node)
        elif block_type == BlockType.PARAGRAPH:
            p_node = md_to_paragraph_html_node(block)
            nodes.append(p_node)
        elif block_type == BlockType.QUOTE:
            q_node = md_to_quote_html_node(block)
            nodes.append(q_node)
        elif block_type == BlockType.UNORDERED:
            ul_node = md_to_unordered_list_html_node(block)
            nodes.append(ul_node)
        elif block_type == BlockType.ORDERED:
            ol_node = md_to_ordered_list_html_node(block)
            nodes.append(ol_node)
        elif block_type == BlockType.CODE:
            code_node = md_to_code_html_node(block)
            nodes.append(code_node)

    # main parent
    div = ParentNode("div", nodes)
    return div.to_html()


# Markdown to Html helper functions
def md_to_heading_html_node(block):
    start_dict = {"h1": 2, "h2": 3, "h3": 4, "h4": 5, "h5": 6, "h6": 7}
    tag = determine_heading_number(block)
    text = block[start_dict[tag] :]
    return LeafNode(tag, text)


def md_to_quote_html_node(block):
    p_nodes = []
    for block in block.split("\n"):
        text = block.strip("> ")
        p_node = md_to_paragraph_html_node(text)
        p_nodes.append(p_node)
    quote_node = ParentNode("blockquote", p_nodes)
    return quote_node


def md_to_paragraph_html_node(block):
    text_nodes = text_to_text_nodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    p = ParentNode("p", html_nodes)
    return p


def md_to_unordered_list_html_node(block):
    item_nodes = []
    for item in block.split("\n"):
        item_node = LeafNode("li", item.strip("- "))
        item_nodes.append(item_node)
    ul_node = ParentNode("ul", item_nodes)
    return ul_node


def md_to_ordered_list_html_node(block):
    item_nodes = []
    for item in block.split("\n"):
        text = item.split(".", 1)[1].strip()
        item_node = LeafNode("li", text)
        item_nodes.append(item_node)
    ol_node = ParentNode("ol", item_nodes)
    return ol_node


def md_to_code_html_node(block):
    code = block.strip("`")
    code_node = LeafNode("code", code)
    pre_node = ParentNode("pre", [code_node])
    return pre_node
