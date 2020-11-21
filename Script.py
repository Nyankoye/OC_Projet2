import requests
from bs4 import BeautifulSoup
import pandas as pd
import shutil
import os


# Fonction pour trouver les liens de toutes les categories de livres du site:"http://books.toscrape.com"
def categoryLinks(url):
    categoryLinksList = []
    ansUrlPage = requests.get(url)
    if ansUrlPage.ok:
        soup = BeautifulSoup(ansUrlPage.text, "html.parser")
        categorySearch = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('li')
        for a in categorySearch:
            category = a.find('a')
            categorylinks = ('http://books.toscrape.com/' + category['href'])
            categoryLinksList.append(categorylinks)
    return categoryLinksList


# Fonction pour trouver des information sur chaques livre et creer un fichier csv
def createBookFile(bookslinks, fileName):
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
    df.to_csv('./Scraping/' + fileName + '.csv', encoding='utf-8-sig')


# Fonction pour trouver les liens de livre de chaque category et creer un fichier csv dans lequel sera stocké les infos des livres trouvés
def createCategoryFile(categoryLinksList):
    bookslinks = []
    nextshow = ""
    for UrlCategory in categoryLinksList:
        ansUrlCategory = requests.get(UrlCategory)
        category = UrlCategory[len('http://books.toscrape.com/catalogue/category/books/'): UrlCategory.find('_')]
        booksSearch = None
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
        createBookFile(bookslinks, category)
        bookslinks = []


# Fonction pour trouver les liens de tous les livres du site: "http://books.toscrape.com"
def booklinks(categoryLinksList):
    bookslinks = []
    nextshow = ""
    for UrlCategory in categoryLinksList:
        ansUrlCategory = requests.get(UrlCategory)
        booksSearch = None
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
    return bookslinks


# Fonction pour trouver liens d'images de livres
def imageLinks(bookslinks):
    linkImageList = []
    for urlBooks in bookslinks:
        ansUrlBooks = requests.get(urlBooks)
        if ansUrlBooks.ok:
            soupBooks = BeautifulSoup(ansUrlBooks.text, "html.parser")
            linkImage = soupBooks.find('div', {'class': 'item active'}).find('img')
            linkImage = str("http://books.toscrape.com/") + linkImage['src'].replace("../../", "")
            linkImageList.append(linkImage)
    return linkImageList


# Fonction pour telecharger les images de livres
def downloadImage(linkImageList):
    for i, linkImageList in enumerate(linkImageList):
        response = requests.get(linkImageList, stream=True)
        with open('./Scraping/images/img' + str(i) + '.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


os.mkdir('Scraping')
os.mkdir('Scraping/images')
urlWebSite = "http://books.toscrape.com"
urlCategory = categoryLinks(urlWebSite)
urlBooks = booklinks(urlCategory)
urlImage = imageLinks(urlBooks)
categoryFile = createCategoryFile(urlCategory)
image = downloadImage(urlImage)
