from split_functions import markdown_to_html_node
import os

def extract_title(markdown):
    markdown = markdown.split("\n")
    first_line = markdown[0]
    if first_line.startswith("# "):
        return first_line[1:].strip()
    else:
        raise Exception("No H1 header!")
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path_content = " "
    with open(from_path, "r") as file:
        from_path_content = file.read()
    node = markdown_to_html_node(from_path_content)
    print(node)
    html_from_path = node.to_html()

    template_path_content = " "
    with open(template_path, "r") as file:
        template_path_content = file.read()

    title = extract_title(from_path_content)

    new_title = template_path_content.replace("{{ Title }}",title)
    new_content = new_title.replace("{{ Content }}",html_from_path)
    
    dest_location = os.path.dirname(dest_path)

    if not os.path.exists(dest_location):
        os.makedirs(dest_location)

    with open(dest_path, "w") as file:
        file.write(new_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_root):
    list_dir = os.listdir(dir_path_content)
    for dir in list_dir:
        subdir_path = os.path.join(dir_path_content, dir)
        if os.path.isdir(subdir_path):
            generate_pages_recursive(subdir_path, template_path, dest_dir_path, content_root)
        else:
            if os.path.splitext(subdir_path)[1] == ".md":
                from_path_content = " "
                with open(subdir_path, "r") as file:
                    from_path_content = file.read()
                node = markdown_to_html_node(from_path_content)
                print(node)
                html_from_path = node.to_html()

                template_path_content = " "
                with open(template_path, "r") as file:
                    template_path_content = file.read()

                title = extract_title(from_path_content)

                new_title = template_path_content.replace("{{ Title }}",title)
                new_content = new_title.replace("{{ Content }}",html_from_path)
                relative_path = os.path.relpath(subdir_path, start=content_root)
                base_name = os.path.splitext(relative_path)[0]  # removes .md
                dest_path = os.path.join(dest_dir_path, base_name + ".html")

                dest_location = os.path.dirname(dest_path)
                if not os.path.exists(dest_location):
                    os.makedirs(dest_location)

                with open(dest_path, "w") as file:
                    file.write(new_content)