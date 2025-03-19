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
		if TextType.TEXT != node.text_type:
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
		
			sections = text.split(f"![{image_alt}]({image_url})", 1)
			
			res.append(TextNode(sections[0],TextType.TEXT))
			
			res.append(TextNode(image_alt,TextType.IMAGE,image_url))

			text = sections[1]
			
	
	return res


def split_nodes_link(old_nodes):
	res = []
	for node in old_nodes:
		if TextType.TEXT != node.text_type:
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
	
			sections = text.split(f"[{link_alt}]({url})", 1)
			res.append(TextNode(sections[0],TextType.TEXT))
			
			res.append(TextNode(link_alt,TextType.LINK,url))

			text = sections[1]
		
	
	return res


def text_to_textnodes(text):
	split_image = split_nodes_image(text)
	split_links = split_nodes_link(node for node in split_image if node.text_type == TextType.TEXT)
	processed_nodes = [node.text for node in split_links if node.text_type == TextType.TEXT]
	remaining_text = " ".join(processed_nodes)  # Start with the full input

	# Process bold text first
	bold_nodes = split_nodes_delimiter(remaining_text, "**")

	# Process remaining text for italics
	italic_nodes = split_nodes_delimiter("".join([node.content for node in bold_nodes if node.type == TextType.TEXT]), "_")

	# Combine results
	res = []
	res.extend(bold_nodes)  # Add all bold nodes
	res.extend(italic_nodes)  # Add all italic nodes
	res.extend(split_image)  # Add all bold nodes
	res.extend(split_links)  # Add all italic nodes






