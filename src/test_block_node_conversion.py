import unittest

from block_node_conversion import *

class TestSplitBlock(unittest.TestCase):
    def test_md_to_blocks(self):
        md = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        res = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertListEqual(
            markdown_to_blocks(md), res
        )

class TestBlockType(unittest.TestCase):
    def test_block_to_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")
    
    def test_block_to_type_ulist(self):
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(block_to_block_type(block), "unordered_list")
    
    def test_block_to_type_small_heading(self):
        block = "#### This is a small heading"
        self.assertEqual(block_to_block_type(block), "heading")
    
    def test_block_to_type_code(self):
        block = "```This is a code```"
        self.assertEqual(block_to_block_type(block), "code")
    
    def test_block_to_type_olist(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        self.assertEqual(block_to_block_type(block), "ordered_list")
    
    def test_block_to_type_normal(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_block_to_type_quote(self):
        block = ">This is quote 1\n>Quote 2\n>Quote3!"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_type_bad_heading(self):
        block = "########## This is an invalid heading"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_type_bad_olist(self):
        block = "1. first\n2. second\n3.wrongly formatted now"
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_convert_variable_types(self):
        md = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* First list item
* Another item
* Last item
'''
        res = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "This is a heading")]),
            ParentNode("p", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it."),
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "First list item")]),
                ParentNode("li", [LeafNode(None, "Another item")]),
                ParentNode("li", [LeafNode(None, "Last item")]),
            ])
        ])
        print(res)
        self.assertEqual(markdown_to_html_node(md), res)
