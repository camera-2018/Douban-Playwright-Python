from playwright.sync_api import sync_playwright
import pandas as pd

df = pd.DataFrame({'bookId': '',
                   'bookName': '',
                   'bookUrl': '',
                   'bookImg': '',
                   'bookAuthor': '',
                   'bookRating': '',
                   'bookRatingPeople': '',
                   'bookIntro': ''
                   }, index=[0])


def getBooks(page):
    global df
    books = []
    bookLists = page.locator('//*[@id="subject_list"]/ul/li')
    count = bookLists.count()

    for i in range(count):
        bookTitle = bookLists.nth(i).locator('div.info > h2 > a')
        bookId = bookTitle.get_attribute('onclick').split("'")[5]
        bookName = bookTitle.inner_text()
        bookUrl = 'https://book.douban.com/subject/{}/'.format(bookId)
        bookImg = bookLists.nth(i).locator('div.pic > a > img').get_attribute('src')
        bookPub = bookLists.nth(i).locator('div.info > div.pub').inner_text()
        bookAuthor = bookPub.split('/')[0]
        bookRating = 'null'
        bookRatingPeople = 'null'

        if bookLists.nth(i).locator('div.info > div.star > span.rating_nums').count() > 0:
            bookRating = bookLists.nth(i).locator('div.info > div.star > span.rating_nums').inner_text()
            bookRatingPeople = bookLists.nth(i).locator('div.info > div.star > span.pl').inner_text().replace(
                '/[^\d]/g', '')
        bookIntro = ''
        if bookLists.nth(i).locator('div.info > p').count() > 0:
            bookIntro = bookLists.nth(i).locator('div.info > p').inner_text()

        book = {
            "bookId": bookId,
            'bookName': bookName,
            'bookUrl': bookUrl,
            'bookImg': bookImg,
            'bookAuthor': bookAuthor,
            'bookRating': bookRating,
            'bookRatingPeople': bookRatingPeople,
            'bookIntro': bookIntro
        }
        # print(book)
        df2 = pd.DataFrame(book, index=[0])
        df = df.append(df2, ignore_index=True)
        books.append(book)
    return books


with sync_playwright() as p:
    books = []
    tagName = '通信'
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://book.douban.com/tag/{}?start=0&type=T'.format(tagName))
    page.once("load", lambda: print("page loaded!"))
    nextButton = page.locator('text=后页>')
    while nextButton.get_attribute('href'):
        books.append(getBooks(page))
        nextButton.click()
        page.locator('//*[@id="db-nav-book"]/div[1]/div/div[1]/a').wait_for()
        if page.locator('text=后页>').count() <= 0:
            break
        nextButton = page.locator('text=后页>')
    books.append(getBooks(page))
    print(df)
    df.to_csv('{}.csv'.format(tagName), index=False, encoding='utf-8')
    browser.close()
