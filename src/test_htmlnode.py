import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        tag = "a"
        value = "Some text"
        props = {"href": "google.com"}
        html_node = HTMLNode(tag, value, props=props)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.value, value)
        self.assertEqual(html_node.props, props)
        self.assertEqual(html_node.children, None)
    
    def test_props_to_html(self):
        tag = "a"
        value = "Some text"
        props = {"href": "google.com", "target": "_blank"}
        html_node = HTMLNode(tag, value, props=props)
        self.assertEqual(html_node.props_to_html(), ' href="google.com" target="_blank"')
    
    def test_children(self):
        tag = "a"
        value = "Some text"
        props = {"href": "google.com"}
        html_node = HTMLNode(tag, value, props=props)
        html_parent = HTMLNode(children=[html_node])
        self.assertEqual(html_parent.children[0], html_node)
    
class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        tag = "a"
        value = "Some text"
        props = {"href": "google.com"}
        leafnode = LeafNode(tag, value, props)
        self.assertEqual(leafnode.tag, tag)
        self.assertEqual(leafnode.value, value)
        self.assertEqual(leafnode.props, props)
        self.assertEqual(leafnode.children, None)

    def test_to_html(self):
        tag = "a"
        value = "Some text"
        props = {"href": "google.com"}
        leafnode = LeafNode(tag, value, props)
        html = leafnode.to_html()
        self.assertEqual(html, '<a href="google.com">Some text</a>')

        