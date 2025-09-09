import unittest

from md_to_html import markdown_to_html_node

MD_1 = """
# This is an H1

This is a short paragraph with some **bold text**.

> A block quote

- Unordered item 1
- Unordered item 2 
- Unordered item 3 
- Unordered item 4 

1. Ordered item 1
2. Ordered item 2 
3. Ordered item 3 
4. Ordered item 4 
"""
HTML_1 = "<div><h1>This is an H1</h1><p>This is a short paragraph with some <b>bold text</b>.</p><blockquote><p>A block quote</p></blockquote><ul><li>Unordered item 1</li><li>Unordered item 2</li><li>Unordered item 3</li><li>Unordered item 4</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li><li>Ordered item 3</li><li>Ordered item 4</li></ol></div>"


class TestMdToHtml(unittest.TestCase):
    def test_simple_md_conversion(self):
        md = MD_1
        expected_html = HTML_1
        actual_html = markdown_to_html_node(md)
        self.assertEqual(actual_html, expected_html)

    def test_md_heading_conversion(self):
        md = """
# Heading one

## Heading two

### Heading three

#### Heading four

##### Heading five 

###### Heading six 

"""
        expected_html = "<div><h1>Heading one</h1><h2>Heading two</h2><h3>Heading three</h3><h4>Heading four</h4><h5>Heading five</h5><h6>Heading six</h6></div>"
        actual_html = markdown_to_html_node(md)
        self.assertEqual(actual_html, expected_html)

    def test_md_ol_conversion(self):
        md = "1. Item one\n2. Item two\n3. Item three"
        expected_html = (
            "<div><ol><li>Item one</li><li>Item two</li><li>Item three</li></ol></div>"
        )
        actual_html = markdown_to_html_node(md)
        self.assertEqual(actual_html, expected_html)

    def test_md_code_conversion(self):
        md = """```
some code here
should retain breaks
```
"""
        expected_html = "<div><pre><code>\nsome code here\nshould retain breaks\n</code></pre></div>"
        actual_html = markdown_to_html_node(md)
        self.assertEqual(actual_html, expected_html)


if __name__ == "__main__":
    unittest.main()
