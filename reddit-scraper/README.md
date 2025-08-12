# Reddit Scraper

A simple Python script to scrape Reddit search results for specific keywords.

## Features

- Scrapes Reddit search results using the old Reddit interface
- Extracts post titles, URLs, text content, scores, and comment counts
- Displays progress with a progress bar
- Outputs structured data for further processing

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

The script currently searches for "marketing agency" posts on Reddit. To search for different terms, modify the `url` variable in `main.py`.

## Output

The script outputs a list of dictionaries containing:
- `title`: Post title
- `post_url`: Link to the Reddit post
- `post_text`: Post content (if available)
- `search_score`: Reddit score/upvotes
- `num_comments`: Number of comments

## Dependencies

- `requests`: HTTP library for making web requests
- `beautifulsoup4`: HTML parsing library
- `tqdm`: Progress bar library

## Note

This scraper uses the old Reddit interface (`old.reddit.com`) which may be more stable for scraping purposes.