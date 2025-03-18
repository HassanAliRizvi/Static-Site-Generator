class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
    
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        
        return result

        """
        for key,value in prop_dict.items():
            return f"{key}={value}"
        """
    
    def __repr__(self):
        return f"Tag: {self.tag} \n Value:{self.value} \n Children:{self.children} Props:{self.props}"
    
#child class - LeafNode; parent class - HTML Node
class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("No value field given")

        if self.tag is None:
            return self.value
    
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None, value=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be None or empty")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Children cannot be None or empty")


        res = f"<{self.tag}>"

        #[p: [LeafNode()]]

        for child in self.children:
            res += child.to_html()
        
        res += f"</{self.tag}>"
        return res



    


    


    
