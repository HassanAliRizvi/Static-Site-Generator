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
	matches = re.findall(r"\!\[(\w+)\]\((.*?)\)",text)
	return matches


def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
	return matches

"""

Functions TO DO
def split_nodes_image(old_nodes):

	#Basically, split the nodes and like do the following

	#find_pattern = str.find(delimiter) 
	#string[find_pattern:len(find_pattern)+1]

	
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

def split_nodes_link(old_nodes):
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







"""