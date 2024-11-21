class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props_str = ''
        if not self.props:
            return props_str
        for key in self.props:
            props_str += f' {key}="{self.props[key]}"'
        return props_str
    
    def __eq__(self, value):
        if not isinstance(value, HTMLNode):
            return NotImplemented
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        html = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html += child.to_html()
        return html + f'</{self.tag}>'