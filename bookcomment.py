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


def get_comments(page):
    comment_content = page.locator('.comment-content').all_inner_texts()
    print(comment_content)
    return comment_content


with sync_playwright() as p:
    comments = []
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://book.douban.com/subject/6709783/comments/')
    page.once("load", lambda: print("page loaded!"))
    nextButton = page.locator('text=后页 >')
    while nextButton.get_attribute('href'):
        comments.append(get_comments(page))
        nextButton.click()
        # page.locator('//*[@id="db-nav-book"]/div[1]/div/div[1]/a').wait_for()
        # if page.locator('text=后页 >').count() <= 0:
        #     break
        # nextButton = page.locator('text=后页 >')
    # comments.append(get_comments(page))
    # print(df)
    # df.to_csv('{}.csv'.format(tagName), index=False, encoding='utf-8')
    browser.close()
    
