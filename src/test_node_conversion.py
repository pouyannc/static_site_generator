import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from node_conversion import * 

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

class TestLinksExtraction(unittest.TestCase):
    def test_extract_image_data(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_link_data(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_functions_no_links(self):
        text = "This text has no links to extract"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

class TestSplitLinks(unittest.TestCase):
    def test_split_image_link(self):
        node = TextNode(
            "This is text with image ![banana](banana.org) and ![pear](pear.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "More text with ![cat](cat.ca) image",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node, node2]),
            [
                TextNode("This is text with image ", TextType.TEXT),
                TextNode("banana", TextType.IMAGE, "banana.org"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "pear", TextType.IMAGE, "pear.com"
                ),
                TextNode("More text with ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.ca"),
                TextNode(" image", TextType.TEXT),
            ]
        )
    
    def test_split_url_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Some more [to github](github.com) links.",
            TextType.TEXT
        )
        self.assertListEqual(
            split_nodes_link([node, node2]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode("Some more ", TextType.TEXT),
                TextNode("to github", TextType.LINK, "github.com"),
                TextNode(" links.", TextType.TEXT),
            ]
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "This is text with without links!",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [node]
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [node]
        )

    def test_split_links_not_text_type(self):
        node = TextNode(
            "This is text a bold text with [link](something.com)...",
            TextType.BOLD,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [node]
        )

    def test_split_links_empty_start(self):
        node = TextNode(
            "[link](something.com)...",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "something.com"),
                TextNode("...", TextType.TEXT),
            ]
        )
    



if __name__ == "__main__":
    unittest.main()