import requests
from bs4 import BeautifulSoup
import os
import urllib

# The URL to scrape
url = "https://docs.quantum.ibm.com/"

# The directory to store files in
output_dir = "./qiskit-docs/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all links to .html files

links = soup.find_all("a", href=True)


for link in links:
    href = link["href"]
    test = "/"
    
    href3 = urllib.parse.urljoin(test, href)
    print(href3)
    # href= urllib.parse.urljoin(href,'"')

    # If it's a .html file
    # print(href)
    href2 = os.path.dirname(href3)
    print(href2)
    href1 = os.path.basename(href3)
    print(href1)
    # print(href)

    if href1 != " ":
        test = ".html"
        href1 = href1 + test
        
    if not href.endswith(".html"):
        if not href.startswith("#"):
            # Make a full URL if necessary
            if not href.startswith("https"):
                file_name = os.path.join(output_dir, href1)
                print(file_name)
                if file_name != "./qiskit-docs/.html":
                    # href = urllib.parse.urljoin(url, href)
                    #  href = url + href
                    href = url + href3
                    print(f"downloading {href}")
                    file_response = requests.get(href)
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(file_response.text)
