import re
import json
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0'}


def remove_consecutive_chars(string):
    pattern = r'[\n\t ]{2,}'
    replaced_string = re.sub(pattern, ' ', string)

    return replaced_string


def crawl(url, domain, visited_urls, visited_titles, first):
    total_content = []

    if url in visited_urls:
        return total_content

    visited_urls.add(url)

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        return total_content

    if not soup.title or soup.title.string in visited_titles:
        return total_content

    visited_titles.add(soup.title.string)

    print(f'Title: {soup.title.string} URL: {url}')

    if first:
        for i, link in enumerate(soup.find_all('a')):
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)

                if domain in urlparse(absolute_url).netloc:
                    total_content.extend(crawl(absolute_url, domain, visited_urls, visited_titles, False))

            if i == 10:
                break

    content = soup.get_text().strip()
    content = remove_consecutive_chars(content)
    total_content.append(content)
    return total_content


def main():
    with open("../data/apify_result.json", 'rb') as file:
        apify_dataset = json.load(file)

    for k, v in apify_dataset.items():
        website = v["website"]
        if website:
            visited_urls = set()
            visited_titles = set()
            domain = urlparse(website).netloc
            total_content = crawl(website, domain, visited_urls, visited_titles, True)
            apify_dataset[k]['content'] = total_content

    with open("../data/apify_result.json", 'w') as file:
        json.dump(apify_dataset, file)


if __name__ == "__main__":
    main()
