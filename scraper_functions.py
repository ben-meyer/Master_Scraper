# Contains the functions to operate the scraper

import datetime
import html2text
import pyperclip
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def initiate_scraper():
    """Requires an input of a list of urls taken from the clipboard
     and returns a cleanly formatted python list of the same urls."""
    # Create the list for the initial urls
    init_urls = []
    # Create a Regular Expression for a web address
    web_address = re.compile(r'http://.*|https://.*')
    # Get the text from the user's clipboard
    text = pyperclip.paste()
    # Extract the url from from the compiled text
    extracted_web_address = web_address.findall(text)
    # Clean up the url strings and store them in the list
    for i in extracted_web_address:
        if i.endswith('\r'):
            init_urls.append(i.replace('\r', ''))
    return init_urls


def scrape_text(init_urls):
    """Requires a clean list of urls, visits each url, scrapes the text and writes a file
    containing the url reference, datetime scraped and the scraped content."""
    # Create a blank dictionary to store page titles and text
    web_page_text_and_title = {}

    # Go through the urls in the list of initialised urls
    # Convert each webpage to text using the html2text module
    # Extract the title of the webpage with BeautifulSoup
    # Store the title of the webpage as a key and the text as a value in the new dictionary
    for url in init_urls:
        try:
            print('Getting: ' + url)
            # get the clean html text
            html = requests.get(url)
            request_text = html.text
            web_page_text = html2text.html2text(request_text)
            # get the page title using Beautiful Soup
            soup = BeautifulSoup(request_text, 'html.parser')
            # strip the title tags off the string
            page_title_tag = soup.find('title')
            page_title = str(page_title_tag)
            page_title = page_title.lstrip('<title>').rstrip('</title>')
            # remove special characters
            page_title = re.sub(r'\W+', '', page_title)
            # store in the dictionary
            web_page_text_and_title[page_title] = web_page_text
        except:
            # if the url can't be reached, remove it from the list so the list is accurate
            # This is why there has to be 2 for loops
            init_urls.remove(url)
            print(f'Received an error. Could not access {url}.')
            print('This url has been removed from the list.')

    # Iterate through the init_urls list again and write the files
    # with the corresponding text and title from the dictionary which was just created.
    for url in init_urls:
        url_number = init_urls.index(url)
        try:
            # Remember - the keys of the dict are the titles of the pages scraped
            file = open(str(list(web_page_text_and_title.keys())[url_number]) + '.txt', "w")
            # Write which page the scraped content belongs to and the datetime scraped
            file.write(f'THIS TEXT CONTENT WAS SCRAPED FROM {url} ON {datetime.now()}\n\n')
            # Remember - the values of the dict is the scraped text content of each page
            file.write(str(list(web_page_text_and_title.values())[url_number]))
            print(f'Writing: {url} as {list(web_page_text_and_title.keys())[url_number]}')
            file.close()
        except:
            print(f'Received an error!\nCould not write content from: {url}')


def scrape_images(init_urls):
    """Requires a clean list of urls. This function visits each url, extracts the image links and
    stores them in a list. Then it removes duplicates from the list and saves each image
    as a numbered file."""
    domain = input('In case of local image links, please provide the full domain name. e.g. '
                   'https://google.com\n\n')

    # Create blank lists to store image links
    web_page_image_links = []
    true_image_links = []

    # Go through the clean urls in the init_urls list.
    # Extract all image links
    for url in init_urls:
        try:
            print('Getting images from: ' + url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            images = soup.find_all('img')
            for i in images:
                link = i['src']
                web_page_image_links.append(link)
        except:
            print('Received an error. Could not access: ' + str(url))

    # If there are local image links, prepend them with the domain provided by the user
    # otherwise, just populate the true list
    for image_link in web_page_image_links:
        if image_link.startswith('/'):
            image_link = f"{domain}{image_link}"
            true_image_links.append(image_link)
        else:
            true_image_links.append(image_link)

    # remove duplicates from list
    true_image_links = list(dict.fromkeys(true_image_links))

    # from the list, assign a number key to each value
    all_image_sources = dict(list(enumerate(true_image_links)))

    for name, image_link in all_image_sources.items():
        try:
            with open(str(name) + '.jpg', 'wb') as f:
                image = requests.get(image_link)
                f.write(image.content)
                print('Writing: ' + image_link + ' as ' + str(name))
        except:
            print(f"Could not write {image_link} as {name}")


def scrape_text_and_images(init_urls):
    scrape_images(init_urls)
    scrape_text(init_urls)