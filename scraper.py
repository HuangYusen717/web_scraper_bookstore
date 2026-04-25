import requests
from bs4 import BeautifulSoup
import csv

# URL pattern example: https://books.toscrape.com/catalogue/page-3.html
BASE_PAGE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
START_PAGE = 1
END_PAGE = 50


def build_page_url(page_number):
    return BASE_PAGE_URL.format(page_number)


def scrape_page(page_number):
    page_url = build_page_url(page_number)

    try:
        response = requests.get(page_url, timeout=10)
    except requests.RequestException:
        return [], False

    if response.status_code != 200:
        return [], False

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    page_data = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        page_data.append({
            'Page': page_number,
            'Title': title,
            'Price': price,
            'Availability': availability
        })

    return page_data, True


def scrape_all_pages(start_page, end_page):
    print(f"Starting scraping pages {start_page} to {end_page}...")

    scraped_data = []
    successful_pages = 0
    failed_pages = 0

    for page_number in range(start_page, end_page + 1):
        print(f"Processing page {page_number}/{end_page}...")
        page_data, succeeded = scrape_page(page_number)

        if not succeeded:
            print(f"Page {page_number} failed: request error or status code issue")
            failed_pages += 1
            continue

        if not page_data:
            print(f"Page {page_number} completed: 0 books")
            successful_pages += 1
            continue

        scraped_data.extend(page_data)
        successful_pages += 1
        print(f"Page {page_number} completed: {len(page_data)} books")

    return scraped_data, successful_pages, failed_pages


def save_to_csv(scraped_data, output_path='data.csv'):
    print(f"\nSaving data to {output_path}...")

    with open(output_path, mode='w', encoding='utf-8-sig', newline='') as file:
        fieldnames = ['Page', 'Title', 'Price', 'Availability']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)


def main():
    scraped_data, successful_pages, failed_pages = scrape_all_pages(START_PAGE, END_PAGE)
    save_to_csv(scraped_data)

    print(
        f"Done! Saved {len(scraped_data)} books to data.csv "
        f"(successful pages: {successful_pages}, failed pages: {failed_pages})"
    )


if __name__ == '__main__':
    main()