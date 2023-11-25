import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

MAX_DEPTH = 1

def get_text_and_html_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(separator=' ')
        cleaned_text = ' '.join(text_content.split())
        print(cleaned_text)
        return cleaned_text, response.text
    else:
        print(f"Error: Unable to fetch content from {url}. Status code: {response.status_code}")
        return None, None
    

def is_valid_url(url):
    ignored_file_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.zip', '.rar']
    return not any(url.endswith(ext) for ext in ignored_file_extensions)


def get_text_from_website(current_url, start_url, visited_urls, depth=0, max_depth=MAX_DEPTH):
    if depth > MAX_DEPTH or current_url in visited_urls:
        return ""

    visited_urls.add(current_url)
    cleaned_text, page_html = get_text_and_html_from_page(current_url)

    if cleaned_text:
        soup = BeautifulSoup(page_html, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            absolute_url = urljoin(current_url, link['href'])
            if is_valid_url(absolute_url) and urlparse(absolute_url).netloc == urlparse(start_url).netloc:
                cleaned_text += get_text_from_website(absolute_url, start_url, visited_urls, depth + 1, max_depth)

    return cleaned_text
