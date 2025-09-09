from enum import Enum

UNKNOWN_BLOCK_ERROR = "ERROR: This is not a known BlockType"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def is_heading_block(block):
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return True
    return False


def is_code_block(block):
    return block.startswith("```") and block.endswith("```")


def is_quote_block(block):
    return all((line.startswith(">") for line in block.split("\n")))


def is_unordered_list_block(block):
    return all((line.startswith("- ") for line in block.split("\n")))


def is_ordered_list_block(block):
    # check if looks like ordered list
    first_check = block.split(". ")
    if not (len(first_check) > 1 and first_check[0] == "1"):
        return False

    count = 1
    is_ordered = False
    for i, line in enumerate(block.split("\n")):
        split_line = line.split(". ")
        if not len(split_line) > 1:
            # Not formated properly
            is_ordered = False
            break
        supposed_num = split_line[0]
        if not supposed_num.isnumeric():
            # Not number
            is_ordered = False
            break
        if not int(supposed_num) == count:
            # not sequential
            is_ordered = False
            break
        count += 1
        is_ordered = True

    return is_ordered


def determine_heading_number(block):
    if block.startswith("# "):
        return "h1"
    elif block.startswith("## "):
        return "h2"
    elif block.startswith("### "):
        return "h3"
    elif block.startswith("#### "):
        return "h4"
    elif block.startswith("##### "):
        return "h5"
    elif block.startswith("###### "):
        return "h6"
    else:
        raise Exception("Unknown heading type")


def block_to_blocktype(block):
    if is_heading_block(block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list_block(block):
        return BlockType.UNORDERED
    elif is_ordered_list_block(block):
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH
