import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from node_conversion import text_node_to_html_node, split_nodes_delimiter

class TestTextToHTML(unittest.TestCase):
    def test_convert_normal_text(self):
        textnode = TextNode('some normal text', TextType.TEXT)
        self.assertEqual(text_node_to_html_node(textnode), LeafNode(None, 'some normal text'))
    
    def test_convert_bold_text(self):
        textnode = TextNode('some bold text', TextType.BOLD)
        self.assertEqual(text_node_to_html_node(textnode), LeafNode('b', 'some bold text'))

    def test_convert_link(self):
        textnode = TextNode('some link', TextType.LINK, "google.com")
        self.assertEqual(text_node_to_html_node(textnode), LeafNode('a', 'some link', {"href": "google.com"}))

class TestSplitDelimiter(unittest.TestCase):
    def test_split_bold(self):
        nodes = [TextNode("this is **bold** text", TextType.TEXT), TextNode("**and even** more **bold** text", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(nodes, '**', TextType.BOLD),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("", TextType.TEXT),
                TextNode("and even", TextType.BOLD),
                TextNode(" more ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
            )
    
    def test_split_code(self):
        nodes = [TextNode("this is `code` text", TextType.TEXT), TextNode("and `code` and `more code` text", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(nodes, '`', TextType.CODE),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
                TextNode("and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ]
            )
    
    def test_invalid_md(self):
        nodes = [TextNode("something **invalid", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)