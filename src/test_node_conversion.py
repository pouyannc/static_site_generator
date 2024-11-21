import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from main import text_node_to_html_node

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