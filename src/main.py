from textnode import *

def main():

    #text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    
    
    """
    split_nodes_link([TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )])
        """

    md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
    """
    #markdown_to_blocks(md)
    md2 = """
        1. One 
        2. Two
        3. Three
        
        """
    md3 = "1. One\n2. Two\n3. Three"
    blocks = block_to_block_type(md3)
    print(blocks)


if __name__ == "__main__":
    main()



