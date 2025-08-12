import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint

url = "https://old.reddit.com/search?q=marketing+agency"

html = requests.get(url)
soup = BeautifulSoup(html.text, "html.parser")

contents_div = soup.find_all("div", class_="contents")[-1]

posts = []

for content in tqdm(contents_div):
    search_result_header = content.find("header", class_="search-result-header")
    a_tag = search_result_header.find("a")
    title = a_tag.text
    post_url = a_tag["href"]
    post_text = None
    search_expando = content.find("div", class_="search-expando collapsed")

    if search_expando:
        search_result_body = content.find("div", class_="search-result-body")
        post_text = search_result_body.text

    search_result_meta = content.find("div", class_="search-result-meta")

    search_score = search_result_meta.find("span", class_="search-score").text
    num_comments = search_result_meta.find("a").text

    posts.append(
        {
            "title": title,
            "post_url": post_url,
            "post_text": post_text,
            "search_score": search_score,
            "num_comments": num_comments,
        }
    )

pprint(posts)
