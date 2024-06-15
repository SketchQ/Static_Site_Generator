from src.textnode import TextNode
from src.splitting_functions import split_nodes_link, split_nodes_image, split_nodes_delimiter

def text_to_textnodes(text):
    from collections import deque

    # Constants for text types
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_image = "image"
    text_type_link = "link"

    # Initial list to hold nodes
    nodes = [TextNode(text, text_type_text)]

    # Split based on images and links first
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Text formatting delimiters and their corresponding types
    formatting_delimiters = [
        ("**", text_type_bold),
        ("*", text_type_italic),
        ("`", text_type_code),
    ]

    # Helper function to split text nodes
    def split_text_nodes(nodes):
        new_nodes = []
        for node in nodes:
            if isinstance(node, TextNode) and node.text_type == text_type_text:
                for delimiter, text_type in formatting_delimiters:
                    node = split_nodes_delimiter([node], delimiter, text_type)
                new_nodes.extend(node)
            else:
                new_nodes.append(node)
        return new_nodes

    # Split text nodes based on formatting delimiters
    nodes = split_text_nodes(nodes)

    return nodes
