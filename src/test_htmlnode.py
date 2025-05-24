import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_nested_paragraphs(self):
        child1 = HTMLNode(tag="p", value="First paragraph")
        child2 = HTMLNode(tag="p", value="Second paragraph")
        parent = HTMLNode(tag="div", children=[child1, child2])
        result = HTMLNode(tag="div", children=[HTMLNode(tag="p", value="First paragraph"), HTMLNode(tag="p", value="Second paragraph")])
        self.assertEqual(parent, result)

    def test_nested_bold(self):
        child1 = HTMLNode(tag="b", value="First Bold")
        child2 = HTMLNode(tag="b", value="Second Bold")
        parent1 = HTMLNode(tag="p", children=[child1, child2])
        result1 = HTMLNode(tag="p", children=[HTMLNode(tag="b", value="First Bold"), HTMLNode(tag="b", value="Second Bold")])
        self.assertEqual(parent1, result1)

    def test_props_to_html(self):
        prop_list = {"href": "https://www.google.com", "target": "_blank"}
        prop_input = HTMLNode(tag="div", props=prop_list, children=[HTMLNode(tag="p", value="First paragraph"), HTMLNode(tag="p", value="Second paragraph")]).props_to_html()
        result = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(prop_input, result)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def props_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = f"<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), result)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK_TEXT, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props_to_html(), " href=\"www.google.com\"")



if __name__ == "__main__":
    unittest.main()