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
    md_split = markdown.split("\n")
    res = []
    i = 0
    while i < len(md_split):
        if md_split[i] != "":
            block = md_split[i].strip()
            i += 1
            while i < len(md_split) and md_split[i] != "":
                block += "\n" + md_split[i].strip()
                i += 1
            res.append(block)
        else:
            i += 1
    return res

md = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
print(md)
for x in markdown_to_blocks(md):
    print(x)
print(markdown_to_blocks(md))