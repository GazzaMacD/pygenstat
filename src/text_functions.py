import re

from textnode import TextType, TextNode


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


def split_nodes_link(nodes_arr):
    find_link_regex = r"(?<!!)\[[^\)]+\)"

    new_nodes = []

    for node in nodes_arr:
        # No link markdown in str
        if not node.text:
            new_nodes.append(node)
            continue
        found = re.search(find_link_regex, node.text)
        if not found:
            new_nodes.append(node)
            continue

        # link markdown in str
        links_removed_list = re.split(find_link_regex, node.text)
        links_details_list = extract_markdown_links(node.text)

        for i, item in enumerate(links_removed_list):
            if not item:
                if i + 1 == len(links_removed_list):
                    break
                else:
                    link_text = links_details_list[i][0]
                    href = links_details_list[i][1]
                    link_node = TextNode(link_text, TextType.LINK, href)
                    new_nodes.append(link_node)
            else:
                if i + 1 == len(links_removed_list):
                    text_node = TextNode(item, TextType.TEXT)
                    new_nodes.append(text_node)
                else:
                    # Add text node
                    text_node = TextNode(item, TextType.TEXT)
                    new_nodes.append(text_node)
                    # Add link node
                    link_text = links_details_list[i][0]
                    href = links_details_list[i][1]
                    link_node = TextNode(link_text, TextType.LINK, href)
                    new_nodes.append(link_node)
    return new_nodes


def split_nodes_image(nodes_arr):
    find_image_regex = r"[!\[]{2}[^\)]+\)"

    new_nodes = []

    for node in nodes_arr:
        # No image markdown in str
        if not node.text:
            new_nodes.append(node)
            continue
        found = re.search(find_image_regex, node.text)
        if not found:
            new_nodes.append(node)
            continue

        # Image markdown in str
        imgs_removed_list = re.split(find_image_regex, node.text)
        imgs_details_list = extract_markdown_images(node.text)

        for i, item in enumerate(imgs_removed_list):
            if not item:
                if i + 1 == len(imgs_removed_list):
                    break
                else:
                    alt_text = imgs_details_list[i][0]
                    src = imgs_details_list[i][1]
                    img_node = TextNode(alt_text, TextType.IMAGE, src)
                    new_nodes.append(img_node)
            else:
                if i + 1 == len(imgs_removed_list):
                    text_node = TextNode(item, TextType.TEXT)
                    new_nodes.append(text_node)
                else:
                    # Add text node
                    text_node = TextNode(item, TextType.TEXT)
                    new_nodes.append(text_node)
                    # Add image node
                    alt_text = imgs_details_list[i][0]
                    src = imgs_details_list[i][1]
                    img_node = TextNode(alt_text, TextType.IMAGE, src)
                    new_nodes.append(img_node)
    return new_nodes


def text_to_text_nodes(text):
    text_node = TextNode(
        text,
        TextType.TEXT,
    )
    nodes = split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter([text_node], "_", TextType.ITALIC),
            "`",
            TextType.CODE,
        ),
        "**",
        TextType.BOLD,
    )
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
