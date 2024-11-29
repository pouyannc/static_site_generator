from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from block_node_conversion import markdown_to_html_node
import os
import shutil
import re

def main():
    build()
    generate_page_recursive("./content", "./template.html", "./public")
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

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content): raise Exception("Content path must be a directory, not a file")
    filenames = os.listdir(dir_path_content)
    for filename in filenames:
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            dest_path = os.path.join(dest_dir_path, "index.html")
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
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            os.mkdir(dest_path)
            generate_page_recursive(from_path, template_path, dest_path)
    return

def extract_title(md):
    matches = re.findall(r"^#\s.*", md)
    if not matches:
        raise Exception("Markdown must have a title (h1) heading to extract document title")
    return matches[0].lstrip("# ")


if __name__ == "__main__":
    main()