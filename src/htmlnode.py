class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        res = ""
        if self.props=={}:
            return ""
        for key,value in self.props.items():
            res += f" {key}=\"{value}\""
        
        return res
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            #raise ValueError
            pass

        if self.tag is None:
            return self.value
        
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No HTML tag!")
        
        if self.children is None:
            raise ValueError("No children!")

        if self.children==[]:
            return f"<{self.tag}></{self.tag}>"

        res = ""

        for child in self.children:
            res += child.to_html()
        
        return f"<{self.tag}>{res}</{self.tag}>"
        
def text_node_to_html_node(text_node):
    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text)
    
    if text_node.text_type.value == "bold":
        return LeafNode("b", text_node.text)
    
    if text_node.text_type.value == "italic":
        return LeafNode("i", text_node.text)

    if text_node.text_type.value == "code":
        return LeafNode("code", text_node.text)

    
    if text_node.text_type.value == "link":
        # "<a href="https://www.google.com">Click me!</a>"
        return LeafNode("a", text_node.text, {"href":text_node.url})

    
    if text_node.text_type.value == "image":
       return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})

        

