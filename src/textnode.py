from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"  # for links like [anchor text](url)
	IMAGE = "image"  # for images like ![alt text](url)

class TextNode():
	def __init__(self,text,text_type,url=None):
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self,other):
		if (
			self.text == other.text and 
			self.text_type == other.text_type and
			self.url == other.url
			):
			return True
		else:
			return False	
	
	# returns a string representation of the TextNode object
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

	def text_node_to_html_node(self,text_node):
		match text_node.text_type:
			case (TextType.TEXT):
				return LeafNode(tag=None, value=text_node.text)
			case (TextType.BOLD):
				return LeafNode(tag="b", value=text_node.text)
			case (TextType.ITALIC):
				return LeafNode(tag="i", value=text_node.text)
			case (TextType.CODE):
				return LeafNode(tag="code", value=text_node.text)
			case (TextType.LINK):
				return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
			case (TextType.IMAGE):
				return LeafNode(tag="img", value="",props={"src":text_node.url, "alt":text_node.text})

			# default case
			# (invalid combination)
			case _:
				return Exception("Not a valid type")
	
#FUNCTION TO CONVERT TEXTNODE TO HTML NODE
#stand alone function
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	res = []
	for node in old_nodes:
		if TextType.TEXT != node.text_type:
			res.append(node)
			continue

		#copy of the text value from node
		
		text = node.text

		opening_delimiter = text.find(delimiter)
		if opening_delimiter == -1:
			res.append(node) 
			continue
		
		closing_delimeter = text.find(delimiter,opening_delimiter+len(delimiter))
		if closing_delimeter == -1:
			raise Exception("Invalid markdown")
		


		# two parts
		text_before_delim = text[:opening_delimiter]
		delimiter_text = text[opening_delimiter+len(delimiter):closing_delimeter]
		text_after_delim = text[closing_delimeter + len(delimiter):]

		res.append(TextNode(text_before_delim,TextType.TEXT))
		res.append(TextNode(delimiter_text,text_type))
		res.append(TextNode(text_after_delim,TextType.TEXT))

	return res

# regex to splut images and links
def extract_markdown_images(text):
	matches = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
	return matches


def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
	return matches


def split_nodes_image(old_nodes):
	res = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			res.append(node)
			continue

		#copy of the text value from node
		text = node.text

		matches = extract_markdown_images(text)
		if not matches:
			res.append(node) 
			continue

		for match in matches:
			image_alt, image_url = match
			res.append(TextNode(image_alt,TextType.IMAGE,image_url))
		
			sections = text.split(f"![{image_alt}]({image_url})", 1)

			
			for section in sections:
			
				res.append(TextNode(section,TextType.TEXT))

			#text = sections[1]
			
	print(res)
	return res

def split_nodes_link(old_nodes):
	res = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			res.append(node)
			continue

		#copy of the text value from node
		text = node.text

		matches = extract_markdown_links(text)
		if not matches:
			res.append(node) 
			continue

		for match in matches:
			link_alt, url = match

			res.append(TextNode(link_alt,TextType.LINK,url))
	
			sections = text.split(f"[{link_alt}]({url})", 1)
			
			for section in sections:
			
				res.append(TextNode(section,TextType.TEXT))
		

			#text = sections[1]
		
	
	return res


def text_to_textnodes(text):
	# Start with a single node
	nodes = [TextNode(text, TextType.TEXT)]

	# Process through each splitting function in sequence
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_image(nodes)	
	nodes = split_nodes_delimitser(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	# Debug - print the nodes to see what's happening
	for i, node in enumerate(nodes):
		print(f"Node {i}: {node.text} ({node.text_type})")
	# Remove any empty text nodes
	nodes = [node for node in nodes if node.text != "" or node.text != " "]

	return nodes






