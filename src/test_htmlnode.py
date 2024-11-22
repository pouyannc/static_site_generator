import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_no_tag_to_html(self):
        leafnode = LeafNode(None, "No tag, just text")
        self.assertEqual(leafnode.to_html(), 'No tag, just text')

class TestParentNode(unittest.TestCase):
    def test_leaf_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parentnode = ParentNode('p', children)
        self.assertEqual(parentnode.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_mixed_children_and_props(self):
        children = [
            ParentNode("div", [LeafNode("i", "italic text"), LeafNode(None, "Normal text")], {"prop": "true"}),
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            
        ]
        parentnode = ParentNode('p', children, {"prop": "true"})
        self.assertEqual(parentnode.to_html(), '<p prop="true"><div prop="true"><i>italic text</i>Normal text</div><b>Bold text</b>Normal text</p>')
    
    def test_nested_parent_children(self):
        children = [
            ParentNode("div", [
                ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
                ]),
        ]
        parentnode = ParentNode('p', children)
        self.assertEqual(parentnode.to_html(), '<p><div><p><b>Bold text</b>Normal text</p><i>italic text</i>Normal text</div></p>')

    def test_no_children(self):
        parentnode = ParentNode('p', None)
        with self.assertRaises(ValueError):
            parentnode.to_html()
    
    def test_no_tag(self):
        parentnode = ParentNode(None, [LeafNode('p', 'leaf')])
        with self.assertRaises(ValueError):
            parentnode.to_html()


if __name__ == "__main__":
    unittest.main()