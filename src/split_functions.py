from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from htmlnode import text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    if old_nodes == "":
        return res
    for node in old_nodes:
        node_text = node.text
        
        if node.text_type != TextType.NORMAL_TEXT:
            res.append(node)
        # This is a **code block** word
        if node.text_type == TextType.NORMAL_TEXT:
            start = node_text.find(delimiter)
            end =  node_text.find(delimiter, start + len(delimiter)-1)
            if start == -1:
                # No delimiter found, add the original node
                res.append(node)
            elif end == -1:
                # Start delimiter found, but no closing delimiter
                raise ValueError("Invalid Markdown")
            else:
                start_word = node_text[0:start]
                start_word_node = TextNode(start_word, TextType.NORMAL_TEXT)
                if start_word:
                    res.append(TextNode(start_word, TextType.NORMAL_TEXT)) 

                delimiter_word = node_text[start + len(delimiter):end]
                if delimiter_word:
                    res.append(TextNode(delimiter_word, text_type))
                
                end_word = node_text[end+len(delimiter):]
                end_word_node = TextNode(end_word, TextType.NORMAL_TEXT)
                print("end word node below......")
                print(end_word_node)
                if end_word:
                    res.extend(split_nodes_delimiter([TextNode(end_word, TextType.NORMAL_TEXT)], delimiter, TextType.NORMAL_TEXT))

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
        #print(f"This is nodes: {nodes}")

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

#used for bold, italic, underline etc
def text_to_textnodes(nodes):
    nodes_list = [TextNode(nodes, TextType.NORMAL_TEXT)]
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
    blocks = markdown_to_blocks(markdown) # ['This is', '-This is list\n-yo']
    
    parent = ParentNode("div",[],None)
    for block in blocks:
        block_type = block_to_block_type(block) # type of block in EACH list #Example: This is paragraph!
        
        #block = TextNode(block,TextType.NORMAL_TEXT,url=None)
        if block_type == BlockType.paragraph:
            block = block.replace('\n', '')
            text_nodes = text_to_textnodes(block)
            children = text_to_children(text_nodes)
            paragraph_node = ParentNode("p", children=children)
            parent.children.append(paragraph_node)
        
        if block_type == BlockType.heading:
            h_tag, text = heading_text(block)
            text_nodes = text_to_textnodes(text)
            children = text_to_children(text_nodes)
            heading_node = ParentNode(f"{h_tag}", children=children)
            parent.children.append(heading_node)

        if block_type == BlockType.quote:
            text = quote_text(block)
            text_nodes = text_to_textnodes(text)
            children = text_to_children(text_nodes)
            heading_node = ParentNode("blockquote", children=children)
            parent.children.append(heading_node)

        if block_type == BlockType.unordered_list:
            text = unordered_list_text(block)
            parent.children.append(text)

        if block_type == BlockType.ordered_list:
            text = ordered_list_text(block)
            parent.children.append(text)

        if block_type == BlockType.code:
            text = code_text(block)
            pre_tag_node = ParentNode("pre", children=[text])
            parent.children.append(pre_tag_node)
    return parent

def heading_text(text):
    count = 0
    word = ""
    i = 0
    text = text
    while i < len(text) and text[i] == "#":
    # what could you do here?
        count += 1
        i += 1
    word = text[count:].lstrip() # so like "#### h1" that's why count + 1
    return f"h{count}",word

def code_text(text):
    code_node = ""
    text = text.split("\n")
    print(text)
    code_counter = 0
    res = ""
    for word in text:
        if word == "```" or word == "`":
            code_counter += 1
        if 0 < code_counter < 2 and word != "```":
            res += word + "\n"
        if code_counter == 2:
            code_node = LeafNode(tag="code",value=res)
            return code_node

def quote_text(text):
    text = text.split("\n")
    res = []
    for word in text:
        res.append(word[1:].lstrip())
    return "\n".join(res)

def unordered_list_text(text):
    text = text.split("\n")
    parent_ul = ParentNode("ul",children=[])
    for word in text:
        word_strip = word[1:].lstrip()
        text_node = text_to_textnodes(word_strip)
        children = text_to_children(text_node)
        unordered_node = ParentNode("li",children=children)
        parent_ul.children.append(unordered_node)
    return parent_ul


def ordered_list_text(text):
    text = text.split("\n")
    parent_ol = ParentNode("ol",[],None)
    for word in text:
        dot_find = word.find(".")
        word_strip = word[dot_find+1:].lstrip()
        text_node = text_to_textnodes(word_strip)
        children = text_to_children(text_node)
        ordered_node = ParentNode("li",children=children)
        parent_ol.children.append(ordered_node)
    return parent_ol

def text_to_children(text_node):
    res = []
    for node in text_node:
        res.append(text_node_to_html_node(node))
        print(node)
    
    return res
    




