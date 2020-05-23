from credentials import GOODREADS_KEY
import requests
import difflib
from bs4 import BeautifulSoup

def isAvailable(availability_link : str, library_to_check : str) -> bool:
    """ Given the link to check availability and library, check if a book is available at the library """
    req = requests.get(availability_link)
    soup =  BeautifulSoup(req.text,'lxml')
    libraries_tags = soup.find_all('td',{'data-caption' : 'Library'})
    for num,library_tags in enumerate(libraries_tags):
        library = library_tags.find('a').find('span').text
        if library == library_to_check:
            availability = soup.find_all('td',{'data-caption' : 'Item Status'})[num].text
            if availability == 'Available':
                return True

def getBooks(book_name : str,author_name : str) -> list:
    """ Get a list of books matching your search query"""
    req = requests.get(f'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/WPAC/BIBENQ?optionsDrop=Full+Catalogue&ENTRY={book_name.replace(" ","+") + "+" + author_name.replace(" ","+")}&ENTRY_NAME=BS&ENTRY_TYPE=K&SORTS=SQL_REL_BIB')
    soup = BeautifulSoup(req.text,'lxml')
    books_elems = soup.find_all('div',{'class' : 'card card-grid'})
    books = []
    for book_elem in books_elems:
        resource_type = book_elem.find('div',{'class' : 'recfrmt-icon'}).get('title')
        if resource_type != 'Books, Manuscripts': continue
        nlb_book_name = book_elem.find('h5',{'class' : 'card-title'}).find('a').get('title')
        author = book_elem.find('span',{'class' : 'd-block'}).text
        try:
            author = author.split(', ')[1] + " " + author.split(', ')[0]
        except:
            author = author_name
        availability_link = 'https://catalogue.nlb.gov.sg' + book_elem.find('a', {'data-toggle' : 'modal'})['href']
        match_ratio = difflib.SequenceMatcher(None,book_name.lower(),nlb_book_name.lower()).ratio()
        match_ratio_author = difflib.SequenceMatcher(None,author,author_name).ratio()
        # print(nlb_book_name,book_name,match_ratio)
        # print(author,author_name,match_ratio_author)
        if match_ratio_author >= 0.9 and match_ratio >= 0.8:
            books.append((nlb_book_name,author,availability_link))
    return books[:5]

def BookData(book : str) -> tuple:
    """ Searches GoodReads for the book and returns title,author and image link """
    url = f"https://www.goodreads.com/search/index.xml?key={GOODREADS_KEY}&q={book.replace(' ','+')}"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    book_data = soup.find('work')
    if book_data == None: return (None,None,None)
    title = book_data.find('title').text.split(' (')[0]
    author = book_data.find('name').text
    image_url = book_data.find('image_url').text
    book = (title,author,image_url)
    return book