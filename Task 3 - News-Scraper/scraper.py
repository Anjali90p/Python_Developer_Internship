import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"
OUTPUT_FILE = "headlines.txt"

def scrape_headlines():
    print(f"Fetching headlines from {URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Finding h2 tags which usually contain headlines on BBC News
    headlines = soup.find_all('h2')
    
    # Use a set to avoid duplicate headlines
    unique_headlines = set()
    for h in headlines:
        text = h.get_text(strip=True)
        # Filter out very short generic UI text
        if text and len(text) > 15:
            unique_headlines.add(text)
    
    # Save the titles in a .txt file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Top Headlines from {URL}\n")
        f.write("="*40 + "\n\n")
        for i, headline in enumerate(unique_headlines, 1):
            f.write(f"{headline}\n")
            
    print(f"Successfully scraped {len(unique_headlines)} headlines and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_headlines()
