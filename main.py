import codecs
import urllib
from io import StringIO
from typing import List
from lxml import etree


def generate_xpath_query(attribute_id: str, html: str):
    """
    Create array of XPaths from a HTML, searching HTML for a attribute_id

    Args:
        `attribute_id`: Zyft ID to search with
        `page_html`: HTML to generate query from

    Returns:
        `x_paths`: List of XPaths
    """
    x_paths: List[str] = []

    # Parse HTML to ElementTree with lxml
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    # Iter all elements of the ElementTree
    for element in tree.iter():

        # Iter the attributes of each element
        for attribute, value in element.items():

            # Check if element has a zyft_node_id
            if attribute == "zyft_node_id" and value == attribute_id:

                # This is the parent path
                path = tree.getpath(element)

                x_paths.append(path)

                # Sub elements of the parent path
                for sub_element in element:
                    sub_element_path = tree.getpath(sub_element)

                    x_paths.append(sub_element_path)

                break
        else:
            continue  # only executed if the inner loop did NOT break
        break  # only executed if the inner loop DID break

    return x_paths


def load_html():
    html_stream = codecs.open("sample-html.html", "r")
    html = html_stream.read()

    # Fetch sample HTML file
    with urllib.request.urlopen("https://dl.dropbox.com/s/u0a8b8o3x86i9id/sample-html-v2.html") as file:
        html: str = file.read().decode("utf-8")
        x_paths = generate_xpath_query("123456", html)

        print("\nX Paths array:")
        print(x_paths, "\n")


if __name__ == "__main__":
    load_html()
