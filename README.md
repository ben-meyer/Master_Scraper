# Master_Scraper
A command line scraper which can scrape images and text.

This file uses the html2text module (https://pypi.org/project/html2text/) to iterate through a list of URLs from a spreadsheet and extract all the text on every webpage.
It can also extract all the images from every webpage, avoiding duplicates. 

**N.B. This program works best and is intended for scraping content off of one domain.**

**Usage**
To use this file:

1. First, create a spreadhseet with one column which lists all the URLs you need to scrape the text or images from. (No headers are necessary, but the URLs must be in a clean format i.e. beginning with http:// or https:// and ending with / or white space).
2. Copy them all to your clipboard.
3. Run the program in your shell or IDE.
4. The program will ask you if you want to scrape images, text or both.

**Output**
The program will save the files it creates to the same directory you run the file from e.g. if the file is located and run from c:\Users\name\Documents\scraper, all the .jpg and .txt files it creates will also be saved there.
