import csv

import requests
from bs4 import BeautifulSoup


def get_page_content(url):
    """
    Takes an url and returns the content of that url in a string
    :param url: string
    :return: string
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    if response.ok:
        return response.text
    print("no content found")
    return ""


def crawl_quotes_website():
    url = "https://quotes.toscrape.com/"

    page_url = url
    while True:
        content = get_page_content(page_url)

        soup = BeautifulSoup(content, "html.parser")

        quotes = soup.select(".quote")
        for quote in quotes:
            quote_text = quote.select_one(".text").getText()
            quote_author = quote.select_one(".author").getText()
            print("****************** Scraping *****************")
            print(quote_text)
            print("By: " + quote_author)
            # csv
            quote_dict = {"Quote": quote_text, "Author": quote_author}

            quote_tags = []
            tags = quote.select(".tag")
            for tag in tags:
                quote_tags.append(tag.getText())

            quote_tags_string = ",".join(quote_tags)
            # print(quote_tags)
            # print(type(quote_tags))
            print(quote_tags_string)
            # print(type(quote_tags_string))
            # csv
            quote_dict["Tags"] = quote_tags_string
            csv_writer.writerow(quote_dict)
            print()

        next_page = soup.select_one(".next > a")
        if next_page is None:
            break
        next_page_url = next_page.get("href")
        page_url = url + next_page_url[1:]
        # print(next_page_url)
        print(page_url)
        print("######################  Next page  ######################")


if __name__ == "__main__":
    # logging

    # csv
    with open("quotes_crawler_with_bs4.csv", "w", newline="", encoding='utf8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Quote", "Author", "Tags"])
        csv_writer.writeheader()

        # craw quotes website
        crawl_quotes_website()
        print("------------------------------------------------------------------")
        print("                       Hey yo! Done.")
        print("-------------------------------------------------------------------")
