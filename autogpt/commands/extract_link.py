import csv
from bs4 import BeautifulSoup
import os

def extract_links_with_labels_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    extracted_links = []
    
    for link in links:
        url = link.get('href')
        label = link.get_text()
        extracted_links.append({'URL': url, 'Label': label})
    
    return extracted_links

def save_links_to_csv(links, chunk_prefix, output_directory, chunk_size = 10):
    # Delete existing chunks if they exist
    existing_chunks = [f for f in os.listdir(output_directory) if f.startswith(chunk_prefix)]
    for chunk_file in existing_chunks:
        os.remove(os.path.join(output_directory, chunk_file))
    
    # Write links to new chunks
    chunk_num = 0
    while len(links) > 0:
        chunk_num += 1
        chunk_links = links[:chunk_size]
        links = links[chunk_size:]
        
        file_name = f"{chunk_prefix}_{chunk_num}.csv"
        file_path = os.path.join(output_directory, file_name)
        
        with open(file_path, 'w', newline='') as file:
            fieldnames = ['URL', 'Label']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(chunk_links)

# Example usage
html = """
<html>
    <body>
        <a href="https://www.example.com/page1">Link 1</a>
        <a href="https://www.example.com/page2">Link 2</a>
        <a href="https://www.example.com/page3">Link 3</a>
        <a href="https://www.example.com/page4">Link 4</a>
        <a href="https://www.example.com/page5">Link 5</a>
        <a href="https://www.example.com/page6">Link 6</a>
        <a href="https://www.example.com/page7">Link 7</a>
        <a href="https://www.example.com/page8">Link 8</a>
        <a href="https://www.example.com/page9">Link 9</a>
        <a href="https://www.example.com/page10">Link 10</a>
    </body>
</html>
"""

# links = extract_links_with_labels_from_html(html)
# chunk_prefix = "links_chunk"
# output_directory = "./data"

# save_links_to_csv(links, chunk_prefix, output_directory, 20)
