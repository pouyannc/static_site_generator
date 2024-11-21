from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

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

def main():
    new_textnode = TextNode("this is a text node", TextType.BOLD, 'https://www.boot.dev')
    print(new_textnode)

    tag = "a"
    value = "Some text"
    props = {"href": "google.com"}
    html_node = HTMLNode(tag, value, props=props)
    print(html_node)

if __name__ == "__main__":
    main()