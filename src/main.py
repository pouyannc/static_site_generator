from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
import os
import shutil

def main():
    build()
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

if __name__ == "__main__":
    main()