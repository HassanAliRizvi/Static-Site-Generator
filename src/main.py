from textnode import *
from split_functions import *
import os
import shutil
from generate_page import generate_page,generate_pages_recursive ,extract_title


def file_transfer(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    def copy_contents(source_dir,dest_dir):
        source_list = os.listdir(source_dir)
        if not os.path.isdir(dest_dir):
            os.mkdir(path=dest_dir)
        for src in source_list:
            src_path = os.path.join(source_dir,src)
            dst_path = os.path.join(dest_dir,src)
            if os.path.isdir(src_path):
                copy_contents(src_path,dst_path)
            else:
                shutil.copy(src_path,dst_path)
    copy_contents(source_dir,dest_dir)

def main():
    
    #node = markdown_to_html_node(md)
    #html = node.to_html()
    #print(html)
    source_dir = "static"
    dest_dir = "public"
    file_transfer(source_dir, dest_dir)
    generate_pages_recursive("content", "template.html", "public", "content")

if __name__ == "__main__":
    main()