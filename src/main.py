from textnode import TextNode
from block_markdown import markdown_to_html_node
from genpage_functions import *
            
def main():
    src_directory = './static'
    dst_directory = './public'

    # Delete the destination directory to ensure idempotency
    delete_directory(dst_directory)

    # Copy contents from source to destination
    copy_contents(src_directory, dst_directory)

    # generate a page
    generate_pages_recursive('./content', 'template.html', './public')


if __name__ == "__main__":
    main()