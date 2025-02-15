import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://coda.io/@latoken/latoken-talent/culture-139"

# Fetch the HTML content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch the website. Status code: {response.status_code}")

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Extract the text content
text_content = soup.get_text(separator="\n")  # Use newlines to separate sections

# Print or save the extracted content
print(text_content)