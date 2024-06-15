import os
import shutil

from block_markdown import markdown_to_html_node

# Generate pages recursively
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Iterate over all files and directories in the current directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            # Check if the file is a markdown file
            if file.endswith('.md'):
                # Construct the full path to the markdown file
                from_path = os.path.join(root, file)
                # Calculate the relative path of the markdown file with respect to the source directory
                relative_path = os.path.relpath(from_path, dir_path_content)
                # Construct the destination path by replacing .md with .html and changing the base directory
                dest_path = os.path.join(dest_dir_path, relative_path)
                dest_path = os.path.splitext(dest_path)[0] + '.html' # replace .md with .html

                # Ensure the directory exists before writing the file
                dest_dir = os.path.dirname(dest_path)
                os.makedirs(dest_dir, exist_ok=True)

                # Generate the HTML page
                generate_page(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def delete_directory(directory):
    # Deletes the specified directory and all its contents.
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Deleted directory: {directory}")

def copy_contents(src_dir, dst_dir):
    # Recursively copies all contents of src_dir to dst_dir.
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)

        if os.path.isfile(src_item):
            try:
                shutil.copy(src_item, dst_item)
                print(f"Copied file: {src_item} to {dst_item}")
            
            except IOError as e:
                print(f"Unable to copy file {src_item}: {e}")
        
        elif os.path.isdir(src_item):
            try:
                copy_contents(src_item, dst_item)
            except Exception as e:
                print(f"Unable to copy directory {src_item}: {e}")