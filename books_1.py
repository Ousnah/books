import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
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

with open('book_info.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                     'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax,
                     number_available, product_description, category, review_rating, image_url])

print("Données envoyées dans 'book_info.csv'")
