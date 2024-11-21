from textnode import TextNode, TextType
from htmlnode import HTMLNode

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