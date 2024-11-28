from inline_node_conversion import *
from htmlnode import ParentNode

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in md_blocks:
        if block == "": continue
        parent_node = None
        block_type = block_to_block_type(block)
        modded_block, tag = strip_md_and_get_tag(block, block_type)
        print(modded_block)
        print(tag)
        if tag == "ul" or tag == "ol":
            list_nodes = []
            for line in modded_block.split("\n"):
                if line == "": continue
                text_nodes = text_to_textnodes(line)
                leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                list_nodes.append(ParentNode("li", leaf_nodes))
            parent_node = ParentNode(tag, list_nodes)
        else:
            text_nodes = text_to_textnodes(modded_block)
            leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            parent_node = ParentNode(tag, leaf_nodes)
            if tag == "code":
                parent_node = ParentNode("pre", [parent_node])
        block_nodes.append(parent_node)
    print(ParentNode("div", block_nodes))
    return ParentNode("div", block_nodes)

def strip_md_and_get_tag(text, type):
    HTML_tag = {
        "heading": "h",
        "code": "code",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "paragraph": "p",
    }

    match type:
        case "heading":
            heading_number = len(text.split(' ', 1)[0])
            return (text.split(' ', 1)[1], f"{HTML_tag[type]}{heading_number}")
        case "code":
            return (text.strip('`'), HTML_tag[type])
        case "quote":
            return ("\n".join(map(lambda x: x[1:], text.split("\n"))), HTML_tag[type])
        case "unordered_list" | "ordered_list":
            return ("\n".join(map(lambda x: x[2:], text.split("\n"))), HTML_tag[type])
        case _:
            return (text, HTML_tag[type])


def block_to_block_type(block):
    split_block = block.split()
    if len(split_block[0]) < 7 and len(split_block[0]) > 0 and "#" in split_block[0] and len(set(split_block[0])) == 1:
        return "heading"
    if (
        block[0:3] == "```"
        and block[-3:] == "```"
        and block[3] != "`"
        and block[-4] != "`"
    ): return "code"
    block_lines = block.split("\n")
    quote = True
    for line in block_lines:
        if line[0] != ">":
            quote = False
            break
    if quote: return "quote"
    ulist = True
    for line in block_lines:
        if line[0:2] != "* " and line[0:2] != "- ":
            ulist = False
            break
    if ulist: return "unordered_list"
    olist = True
    for i in range(len(block_lines)):
        if block_lines[i][0:3] != f"{i+1}. ":
            olist = False
            break
    if olist: return "ordered_list"
    return "paragraph"


def markdown_to_blocks(markdown):
    md_split = markdown.split("\n\n")
    res = []
    for block in md_split:
        if block == "":
            continue
        block = block.strip()
        res.append(block)
    return res
