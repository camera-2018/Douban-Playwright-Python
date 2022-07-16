from playwright.sync_api import sync_playwright
import pandas as pd

bookDetailsList = []
bookList = pd.read_csv('通信.csv', encoding='utf-8').drop(index=0)
df = pd.DataFrame({'作者': '',
                   '出版社': '',
                   '出版年': '',
                   '页数': '',
                   '定价': '',
                   '装帧': '',
                   'ISBN': '',
                   '简介': '',
                   '书名': '',
                   '图片': '',
                   }, index=[0])


def getBookDetails(page):
    bookDetails = {}
    objectList = {}
    bookName = page.locator('//*[@id="wrapper"]/h1/span').inner_text()
    bookImg = page.locator('//*[@id="mainpic"]/a/img').get_attribute('src')
    bookDetailList = (page.locator('//*[@id="info"]').all_inner_texts())[0].split('\n')
    for item in bookDetailList:
        item = item.replace('/\s/g', '')
        if ':' in item:
            key = item.split(':')[0]
            value = item.split(':')[1]
            objectList[key] = value.strip()

    if page.locator('#link-report > .short > .intro > p > .a_show_full').count() > 0:
        page.locator('#link-report > .short > .intro > p > .a_show_full').click()

    intro = page.locator('#link-report').all_inner_texts()
    objectList['简介'] = '\n'.join(intro)
    bookDetails = objectList
    bookDetails['书名'] = bookName
    bookDetails['图片'] = bookImg
    return bookDetails


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    for i in range(len(bookList)):
        bookDetailUrl = bookList['bookUrl'][i + 1]
        page.goto(bookDetailUrl)
        bookDetails = getBookDetails(page)
        print(bookDetails)
        bookDetailsList.append(bookDetails)
        df2 = pd.DataFrame(bookDetails, index=[0])
        df = df.append(df2, ignore_index=True)
    df = df.drop(index=0)
    df.to_csv('通信detail.csv', encoding='utf-8')
    df.to_excel('通信detail.xlsx')
