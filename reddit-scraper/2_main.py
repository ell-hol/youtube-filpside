import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint
import urllib.parse
from utils import save_json
import time
from tenacity import retry


def get_url_from_params(params: dict = {"q": "marketing agency"}) -> str:
    base_url = "https://old.reddit.com/search?{encoded_params}"
    encoded_params = urllib.parse.urlencode(params)
    return base_url.format(encoded_params=encoded_params)


def get_main_soup_from_url(url: str) -> BeautifulSoup:
    html = requests.get(url)
    return BeautifulSoup(html.text, "html.parser")


def preprocess_number_string(number_str: str) -> str:
    return number_str.replace(",", "")


def preprocess_score(score: str) -> int:
    return int(preprocess_number_string(score).replace("points", "").replace("point", ""))


def preprocess_num_comments(num_comments: str) -> int:
    return int(preprocess_number_string(num_comments).replace("comments", "").replace("comment", ""))


# @retry
def scrape_posts_from_params(params={"q": "marketing agency"}, pages=5):
    posts = []

    url = get_url_from_params(params)

    print(url)

    for page in tqdm(range(1, pages), unit="page", leave=True):
        soup = get_main_soup_from_url(url)

        print(soup)

        body = soup.find("body")

        nextprev_span = body.find_all("span", {"class": "nextprev"})

        assert False

        contents_divs = body.find_all("div", {"class": "contents"})
        if contents_divs:
            contents_divs = contents_divs[-1]
        else:
            contents_divs = soup.find_all("div", class_="search-result-group")[-1]

        # print(f"found {len(contents_divs)} search results in page {page}")

        for content in tqdm(contents_divs, desc=f"scraping {url}", unit="search result", leave=False):
            search_result_header = content.find_all("header", class_="search-result-header")[0]
            a_tag = search_result_header.find("a")
            title = a_tag.text
            post_url = a_tag["href"]
            post_text = None
            search_expando = content.find("div", class_="search-expando collapsed")

            if search_expando:
                search_result_body = content.find("div", class_="search-result-body")
                post_text = search_result_body.text

            search_result_meta = content.find("div", class_="search-result-meta")

            search_score = search_result_meta.find("span", class_="search-score")
            search_score = search_score.text if search_score else None
            search_score_int = preprocess_score(search_score) if search_score else -1

            num_comments = search_result_meta.find("a").text
            num_comments_int = preprocess_num_comments(num_comments)

            author = search_result_meta.find("span", class_="search-author")
            author_tag = author.find("a")
            author_name = author_tag.text
            author_url = author_tag["href"]

            subreddit = search_result_meta.find("a", class_="search-subreddit-link may-blank")
            subreddit_name = subreddit.text
            subreddit_url = subreddit["href"]

            posts.append(
                {
                    "title": title,
                    "post_url": post_url,
                    "post_text": post_text,
                    "search_score": search_score_int,
                    "num_comments": num_comments_int,
                    "author_name": author_name,
                    "author_url": author_url,
                    "subreddit_name": subreddit_name,
                    "subreddit_url": subreddit_url,
                }
            )
            time.sleep(1)

        # nextprev_span = body.find_all("span", {"class": "nextprev"})
        # url = nextprev_span.find("a")
        # print(nextprev_span)

    return posts


def main():
    # search_params = {"q": "why is it so hard to get users", "sort": "new", "t": "day", "restrict_sr": ""}  # newest - last 24h
    search_params = {
        "q": "SaaS scraping",
        "restrict_sr": "",
        "sort": "relevance",
        # "t": "all",
    }  # most relevant - last 24h
    # search_params = {"q": "vercel pricing", "sort": "top"}  # best
    posts = scrape_posts_from_params(search_params)

    # Sort by search score descending
    posts = sorted(posts, key=lambda post: post["search_score"], reverse=True)
    save_json(posts)


if __name__ == "__main__":
    main()
