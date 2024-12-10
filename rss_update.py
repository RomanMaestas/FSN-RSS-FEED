import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

# URL of the sports news RSS feed (adjust as needed)
NEWS_URL = 'https://www.soccernews.com/category/uefa-champions-league/feed/'

def fetch_news():
    # Fetch content from the RSS feed
    print(f"Fetching news from {NEWS_URL}...")
    try:
        response = requests.get(NEWS_URL)
        response.raise_for_status()  # Ensure we get a valid response
        print("Response received successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the news feed: {e}")
        return []

    # Parse the RSS feed using lxml for reliability
    soup = BeautifulSoup(response.text, 'lxml-xml')

    # Extract articles from the RSS feed
    items = soup.find_all('item')  # 'item' is typically used in RSS feeds
    print(f"Found {len(items)} articles.")  # Debugging: print number of articles found
    
    news_items = []

    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text
        pub_date = item.find('pubDate').text if item.find('pubDate') else datetime.now()

        news_items.append({
            'title': title,
            'url': link,
            'description': description,
            'pubDate': pub_date
        })

    return news_items

def create_rss(news_items):
    if not news_items:
        print("No news items to create RSS feed.")
        return
    
    fg = FeedGenerator()
    fg.title('FSN Sports News Feed')
    fg.link(href='https://romanmaestas.github.io/FSN-RSS-FEED/fubo_rss.xml', rel='self')
    fg.description('Latest sports news for BKFC and UEFA')

    print(f"Creating {len(news_items)} feed entries...")  # Debugging: print how many entries are being created

    for item in news_items:
        fe = fg.add_entry()
        fe.title(item['title'])
        fe.link(href=item['url'])
        fe.description(item['description'])
        fe.pubDate(item['pubDate'])

    try:
        fg.rss_file('fubo_rss.xml')
        print("RSS file created successfully!")  # Debugging: confirm RSS file creation
    except Exception as e:
        print(f"Error creating RSS file: {e}")

# Fetch and create the feed
news_items = fetch_news()
if news_items:
    create_rss(news_items)
    print("RSS feed updated!")
else:
    print("No news to update.")


