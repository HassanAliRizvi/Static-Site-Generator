from textnode import *

def main():
    text_node = TextNode("This is some regular text", TextType.TEXT, None)
    print(text_node)
    text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    text_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) hello",
            TextType.TEXT,
        )
    split_nodes_image([text_node])



if __name__ == "__main__":
    main()



