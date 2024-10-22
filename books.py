import requests
from bs4 import BeautifulSoup
import csv

def extract_book_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_page_url = url
    upc = soup.find('table', class_='table table-striped').find_all('td')[0].get_text()
    title = soup.find('h1').get_text()
    price_including_tax = soup.find('table', class_='table table-striped').find_all('td')[3].get_text()
    price_excluding_tax = soup.find('table', class_='table table-striped').find_all('td')[2].get_text()
    number_available = soup.find('table', class_='table table-striped').find_all('td')[5].get_text()
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('a')[2].get_text()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = "https://books.toscrape.com/" + soup.find('img')['src'].replace('../', '')

    return {
            'product_page_url': product_page_url,
            'upc': upc,
            'title': title,
            'price_including_tax': price_including_tax,
            'price_excluding_tax': price_excluding_tax,
            'number_available': number_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url
    }

def extract_category_book_urls(category_url):
    book_urls = []
    page_num = 1
    base_url = category_url.rsplit('/', 1)[0]

    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('h3'):
            book_partial_url = link.find('a')['href']
            book_full_url = "https://books.toscrape.com/catalogue/" + book_partial_url.replace('../../../', '')
            book_urls.append(book_full_url)
            
            next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = base_url + '/' + next_page_url
        else:
            break

    return book_urls

category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

book_urls = extract_category_book_urls(category_url)
with open('book_info.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                     'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    writer.writeheader()

    for book_url in book_urls:
        book_data = extract_book_data(book_url)
        writer.writerow(book_data)

print("Données envoyées dans 'book_info.csv'")
