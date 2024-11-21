from textnode import TextNode, TextType

def main():
    new_textnode = TextNode("this is a text node", TextType.BOLD, 'https://www.boot.dev')
    print(new_textnode)

if __name__ == "__main__":
    main()