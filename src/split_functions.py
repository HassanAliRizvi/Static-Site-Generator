from textnode import TextNode
from textnode import TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        node_text = node.text
        
        if node.text_type != TextType.NORMAL_TEXT:
            res.append(node)
        # This is a **code block** word
        if node.text_type == TextType.NORMAL_TEXT:
            start = node_text.find(delimiter)
            end =  node_text.find(delimiter, start + len(delimiter))
            if start == -1:
                # No delimiter found, add the original node
                res.append(node)
            elif end == -1:
                # Start delimiter found, but no closing delimiter
                raise ValueError("Invalid Markdown")
            else:
                start_word = node_text[0:start]
                start_word_node = TextNode(start_word, TextType.NORMAL_TEXT)
                res.append(start_word_node) 

                delimiter_word = node_text[start + len(delimiter):end]

                delim_res = TextNode(delimiter_word, text_type)
                res.append(delim_res)  
                
                end_word = node_text[end+len(delimiter):]
                end_word_node = TextNode(end_word, TextType.NORMAL_TEXT)
                res.append(end_word_node)

    return res

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches
    

def extract_markdown_link(link):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", link)
    return matches

def split_nodes_image(old_nodes):
    res = []
    # list -> tuple
    nodes_for_image = old_nodes
    for nodes in nodes_for_image:
        #print(f"This is the node {nodes}")

        if nodes.text_type != TextType.NORMAL_TEXT:
            res.append(nodes)
            continue
        
        remaining_text = nodes.text
        
        image_extract = extract_markdown_images(remaining_text)

        if len(image_extract) == 0:
            res.append(nodes)
            continue

        for image in image_extract:
        
            alt, link = image
            split_node = remaining_text.split(f"![{alt}]({link})",1)
            # [This is text with an, ![image](https......) , and another ![]() and another ![](www.)]
            # [This is text with an, and another ![]() and another ![](www.)]
            if split_node[0] != "":
                res.append(TextNode(split_node[0],TextType.NORMAL_TEXT))
            
            res.append(TextNode(alt,TextType.IMAGE_TEXT, link))

            remaining_text = split_node[1]
        
        if remaining_text != "":
            res.append(TextNode(remaining_text,TextType.NORMAL_TEXT))
        
    return res


def split_nodes_link(old_nodes):

    res = []
    # list -> tuple
    nodes_for_image = old_nodes
    for nodes in nodes_for_image:
        #print(f"This is the node {nodes}")

        if nodes.text_type != TextType.NORMAL_TEXT:
            res.append(nodes)
            continue
        
        remaining_text = nodes.text
        
        link_extract = extract_markdown_link(remaining_text)

        if len(link_extract) == 0:
            res.append(nodes)
            continue

        for links in link_extract:
        
            alt, link = links
            split_node = remaining_text.split(f"[{alt}]({link})",1)
            # [This is text with an, ![image](https......) , and another ![]() and another ![](www.)]
            # [This is text with an, and another ![]() and another ![](www.)]
            if split_node[0] != "":
                res.append(TextNode(split_node[0],TextType.NORMAL_TEXT))
            
            res.append(TextNode(alt,TextType.LINK_TEXT, link))

            remaining_text = split_node[1]
        
        if remaining_text != "":
            res.append(TextNode(remaining_text,TextType.NORMAL_TEXT))
        
    return res

def text_to_textnodes(nodes):
    nodes_list = [nodes]
    nodes = split_nodes_image(nodes_list)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    
    return nodes

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    res = []
    splt_word = markdown.split("\n\n")
    #print(splt_word)
    for word in splt_word:
        word_strip = word.strip()
        #print(word_strip)
        word_splt = word_strip.split("\n")
        #print(word_splt)
        cleaned_list = []
        for word in word_splt:
            cleaned_list.append(word.strip())
        res.append("\n".join(cleaned_list))
        

    return res


# Block Types: Seeing which block type matches heading, paragraph etc...

from enum import Enum

class BlockType(Enum):
	paragraph = "paragraph"
	heading = "heading"
	code = "code"
	quote = "quote"
	unordered_list = "unordered_list"
	ordered_list = "ordered_list"

def block_to_block_type(markdown_text):
    
    text_split = markdown_to_blocks(markdown_text)
    for word in text_split:
        if word.startswith("#"):
            return BlockType.heading
        
        if word.startswith("```") and word.endswith("```"):
            return BlockType.code
        
        if word.startswith(">"):
            word_splt = word.split("\n")
            word_bool = True
            for wrd in word_splt:
                if not wrd.startswith(">"):
                    word_bool = False
                    break
                
            if word_bool == True:
                return BlockType.quote

        if word.startswith("- "):
            word_splt = word.split("\n")
            word_bool = True
            for wrd in word_splt:
                if not wrd.startswith("- "):
                    word_bool = False
                    break
            if word_bool == True:
                return BlockType.unordered_list

        if word.split("\n")[0].startswith("1. "):
            word_splt = word.split("\n")
            word_bool = True
            for count in range(len(word_splt)):
                if not word_splt[count].startswith(f"{count+1}. "):
                    word_bool = False
                    break
            if word_bool == True:
                return BlockType.ordered_list
            
    return BlockType.paragraph    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_type = block_to_block_type(markdown)

    if block_type == BlockType.paragraph:
        paragraph_text(blocks)

    if block_type == BlockType.heading:
        heading_text(blocks)

    if block_type == BlockType.code:
        code_text(blocks)

    if block_type == BlockType.quote:
        quote_text(blocks)

    if block_type == BlockType.unordered_list:
        unordered_list_text(blocks)

    if block_type == BlockType.ordered_list:
        ordered_list_text(blocks)

    
    def paragraph_text(blocks_list):
        pass

    def heading_text(blocks_list):
        pass

    def code_text(blocks_list):
        pass

    def quote_text(blocks_list):
        pass

    def unordered_list_text(blocks_list):
        pass

    def ordered_list_text(blocks_list):
        pass



