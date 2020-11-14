import requests
from bs4 import BeautifulSoup
import pandas as pd


infos = []
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
ansUrlBooks = requests.get(url)
if ansUrlBooks.ok:
    soupBooks = BeautifulSoup(ansUrlBooks.text, "html.parser")
    td = soupBooks.find('table', {'class': 'table table-striped'}).findAll('td')
    p = soupBooks.findAll('p')
    ul = soupBooks.find('ul', {'class': 'breadcrumb'}).findAll('li')
    product_page_url = url
    universal_product_code = td[0].text
    price_including_tax = td[3].text
    price_excluding_tax = td[2].text
    number_available = td[5].text
    product_description = p[3].text
    category = ul[2].text.strip()
    title = soupBooks.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
    rating = soupBooks.find('div', {'class': 'col-sm-6 product_main'}).find('p', 'star-rating')['class'][-1]
    linkImage = soupBooks.find('div', {'class': 'item active'}).find('img')
    linkImage = str("http://books.toscrape.com/") + linkImage['src'].replace("../../", "")
    output = {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'Titre': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'Lien Image': linkImage,
        'Rate': rating,
    }
    infos.append(output)
    df = pd.DataFrame(infos)
    print(df.head())
    df.to_csv(category + '.csv', encoding='utf-8-sig')
    print(output)
else:
    print("Impossible de se connecter")
