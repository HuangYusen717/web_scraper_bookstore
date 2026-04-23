import requests
from bs4 import BeautifulSoup
import csv

# URL pattern example: https://books.toscrape.com/catalogue/page-3.html
BASE_PAGE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
START_PAGE = 1
END_PAGE = 50


def build_page_url(page_number):
    return BASE_PAGE_URL.format(page_number)


print(f"Starting scraping pages {START_PAGE} to {END_PAGE}...")

# prepare a list to store all scraped books from all pages
scraped_data = []
successful_pages = 0
failed_pages = 0

for page_number in range(START_PAGE, END_PAGE + 1):
    page_url = build_page_url(page_number)
    print(f"Processing page {page_number}/{END_PAGE}...")

    try:
        response = requests.get(page_url, timeout=10)
    except requests.RequestException as exc:
        print(f"Page {page_number} failed: request error")
        failed_pages += 1
        continue

    if response.status_code != 200:
        print(f"Page {page_number} failed: status code {response.status_code}")
        failed_pages += 1
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    if not books:
        print(f"Page {page_number} completed: 0 books")
        successful_pages += 1
        continue

    # extract and store each book's information
    page_books_count = 0
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        scraped_data.append({
            'Page': page_number,
            'Title': title,
            'Price': price,
            'Availability': availability
        })
        page_books_count += 1

    successful_pages += 1
    print(f"Page {page_number} completed: {page_books_count} books")

print("\nSaving data to data.csv...")
with open('data.csv', mode='w', encoding='utf-8-sig', newline='') as file:
    fieldnames = ['Page', 'Title', 'Price', 'Availability']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scraped_data)

print(
    f"Done! Saved {len(scraped_data)} books to data.csv "
    f"(successful pages: {successful_pages}, failed pages: {failed_pages})"
)