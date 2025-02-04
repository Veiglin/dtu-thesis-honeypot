import requests
import os
import sys
from bs4 import BeautifulSoup

def clone_page(url, output_path='src/cloner/output.html'):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (status codes 4xx/5xx)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    html_content = response.text

    # Use BeautifulSoup to parse and prettify the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    prettified_html = soup.prettify()

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    # Write the prettified HTML to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prettified_html)

    print(f"Cloned page saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clone_page.py <URL> <output_file>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"src/templates/{url.split('//')[-1].split('.')[1].split('/')[0]}.html"
    clone_page(url, output_file)
