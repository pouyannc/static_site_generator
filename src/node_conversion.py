from htmlnode import LeafNode
from textnode import TextNode, TextType
import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        old_type = old_node.text_type
        if old_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        i = 0
        node_arr = old_node.text.split(delimiter)
        if len(node_arr) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        for node_text in node_arr:
            if node_text == "":
                i += 1
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(node_text, old_type))
            else:
                new_nodes.append(TextNode(node_text, text_type))
            i += 1
    return new_nodes

def text_node_to_html_node(text_node):
    match text_node.text_type.value:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode('b', text_node.text)
        case "italic":
            return LeafNode('i', text_node.text)
        case "code":
            return LeafNode('code', text_node.text)
        case "link":
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid text type")