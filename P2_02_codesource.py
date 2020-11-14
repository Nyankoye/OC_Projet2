import requests
from bs4 import BeautifulSoup
import pandas as pd

bookslinks = []
nextshow = ""
infos = []
UrlCategory = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"


# Fonction pour trouver des information sur chaques livre et creer un fichier csv
def createBookFile(bookslinks):
    infos = []
    for urlBooks in bookslinks:
        ansUrlBooks = requests.get(urlBooks)
        if ansUrlBooks.ok:
            soupBooks = BeautifulSoup(ansUrlBooks.text, "html.parser")
            td = soupBooks.find('table').findAll('td')
            p = soupBooks.findAll('p')
            ul = soupBooks.find('ul', {'class': 'breadcrumb'}).findAll('li')
            product_page_url = urlBooks
            universal_product_code = td[0].text
            price_including_tax = td[3].text
            price_excluding_tax = td[2].text
            number_available = td[5].text
            product_description = p[3].text
            categoryBook = ul[2].text.strip()
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
                'category': categoryBook,
                'Lien Image': linkImage,
                'Rate': rating,
            }
            infos.append(output)
    df = pd.DataFrame(infos)
    print(df.head())
    df.to_csv(categoryBook + '.csv', encoding='utf-8-sig')

ansUrlCategory = requests.get(UrlCategory)
if ansUrlCategory.ok:
    soup = BeautifulSoup(ansUrlCategory.text, "html.parser")
    booksSearch = soup.findAll('article')
    nextshow = soup.find('li', {'class': 'next'})
for article in booksSearch:
    a = article.find('a')
    link = a['href']
    bookslinks.append('http://books.toscrape.com/catalogue/' + link.replace("../../../", ''))
    # Boucle pour trouver les liens de la page suivante
    while nextshow is not None:
        nextPage = nextshow.find('a')
        linkNext = nextPage['href']
        nextPageLink = (UrlCategory.replace("index.html", "") + linkNext.replace("../../../", ''))
        ansNextPage = requests.get(nextPageLink)
        if ansNextPage.ok:
            soupNext = BeautifulSoup(ansNextPage.text, "html.parser")
            booksNextPage = soupNext.findAll('article')
            nextshow = soupNext.find('li', {'class': 'next'})
        for d in booksNextPage:
            searchNextBooks = d.find('a')
            linkNextBooks = searchNextBooks['href']
            bookslinks.append('http://books.toscrape.com/catalogue/' + linkNextBooks.replace("../../../", ''))
createBookFile(bookslinks)
