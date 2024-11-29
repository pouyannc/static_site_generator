from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from block_node_conversion import markdown_to_html_node
import os
import shutil
import re

def main():
    build()
    generate_page("./content/index.md", "./template.html", "./public/index.html")
    return

def build():
    print("Current working directory:", os.getcwd())
    if os.path.exists("./public"):
        print("Removing current public directory...")
        shutil.rmtree("./public")
    os.mkdir("./public")  
    print("Copying contents to public: ", os.listdir("./static"))
    copy_files_r("./static", "./public")
    return

def copy_files_r(source, dest):
    if os.path.isfile(source):
        print("Cannot copy contents of a file (path to file given)")
        return

    contents = os.listdir(source)
    for item in contents:
        source_path = os.path.join(source, item)
        if os.path.isfile(source_path):
            print("file copied:", shutil.copy(source_path, dest))
        else:
            dest_path = os.path.join(dest, item)
            os.mkdir(dest_path)
            copy_files_r(source_path, dest_path)
    return

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as md_file:
        md = md_file.read()
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    with open(template_path) as template_file:
        template = template_file.read()
    title = extract_title(md)
    index_html = template.replace("{{ Content }}", html)
    index_html = index_html.replace("{{ Title }}", title)
    with open(dest_path, "w") as dest_file:
        dest_file.write(index_html)

def extract_title(md):
    matches = re.findall(r"^#\s.*", md)
    if not matches:
        raise Exception("Markdown must have a title (h1) heading to extract document title")
    return matches[0].lstrip("# ")


if __name__ == "__main__":
    main()