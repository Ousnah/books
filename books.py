import requests, csv, os
from bs4 import BeautifulSoup

base_url = 'https://books.toscrape.com/'

def download_image(image_url, category, title):
    response = requests.get(image_url)
    image_folder = 'images/{category}'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
        print(f"Dossier '{image_folder}' créé avec succès.")

    image_filename = f"{image_folder}/{title.replace(' ', '_').replace('/', '-')}.jpg"

    with open(image_filename, 'wb') as img_file:
        img_file.write(response.content)
    print(f"Image téléchargée : {image_filename}")
def extract_book_data(url, category):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_page_url = url
    upc = soup.find('table', class_='table table-striped').find_all('td')[0].get_text()
    title = soup.find('h1').get_text()
    price_including_tax = soup.find('table', class_='table table-striped').find_all('td')[3].get_text()
    price_excluding_tax = soup.find('table', class_='table table-striped').find_all('td')[2].get_text()
    number_available = soup.find('table', class_='table table-striped').find_all('td')[5].get_text()
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = "https://books.toscrape.com/" + soup.find('img')['src'].replace('../', '')

    download_image(image_url, category, title)

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
def extract_categories():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = {}
    category_list = soup.find('ul', class_='nav-list').find('ul').find_all('li')

    for category in category_list:
        category_name = category.get_text().strip()
        category_url = base_url + category.find('a')['href']
        categories[category_name] = category_url

    return categories

def scrape_all_categories():
    categories = extract_categories()

    for category, category_url in categories.items():
        print(f"Scraping la catégorie : {category}")

        book_urls = extract_category_book_urls(category_url)
        csv_filename = f"{category.replace(' ', '_').replace('/', '-')}.csv"

        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                                                     'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
            writer.writeheader()

            for book_url in book_urls:
                book_data = extract_book_data(book_url, category)
                writer.writerow(book_data)

        print(f"Données pour la catégorie '{category}' enregistrées dans '{csv_filename}'.")

scrape_all_categories()

category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

print("Données envoyées dans 'book_info.csv'")
