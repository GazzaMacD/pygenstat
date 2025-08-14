import unittest
from blocks import BlockType, block_to_blocktype


class TestBlocksToBlockType(unittest.TestCase):
    def test_heading_type_block(self):
        blocks = [
            "# This is an h1",
            "## This is an h2",
            "### This is a h3",
            "#### This is an h4",
            "##### This is an h5",
            "###### This is an h6",
            "This is a paragraph",
        ]
        expected = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual([block_to_blocktype(block) for block in blocks], expected)

    def test_code_type_block(self):
        blocks = [
            "###### This is an h6",
            "```some code```",
            "This is a paragraph",
        ]
        expected = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual([block_to_blocktype(block) for block in blocks], expected)

    def test_quote_type_block(self):
        blocks = [
            "###### This is an h6",
            "```some code```",
            "> This is a quote",
            "> This is multiline\n> quote.",
            "This is a paragraph",
        ]
        expected = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual([block_to_blocktype(block) for block in blocks], expected)

    def test_unordered_type_block(self):
        blocks = [
            "###### This is an h6",
            "```some code```",
            "> This is a quote",
            "> This is multiline\n> quote.",
            "- item one\n- item two\n- item three",
            "This is a paragraph",
        ]
        expected = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.UNORDERED,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual([block_to_blocktype(block) for block in blocks], expected)

    def test_ordered_type_block(self):
        blocks = [
            "###### This is an h6",
            "1. First item\n2. Second item\n3. Third item",
            "2. First item\n3. Second item\n4. Third item",  # Should fail as not starting at 1
            "1. First item\n2. Second item\n4. Third item",  # Should fail as not increment by one
            "1.First item\n2.Second item\n3. Third item",  # Should fail as no space after .
            "This is a paragraph",
        ]
        expected = [
            BlockType.HEADING,
            BlockType.ORDERED,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
        ]
        actual = [block_to_blocktype(block) for block in blocks]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
