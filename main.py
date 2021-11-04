import scraper_functions

# Ask the user if they want to scrape images, text or both
print('Hello! I am a web scraping program. I can scrape images and text from a list of urls.')
print('Would you like to scrape images, text, or both?\n')
operation = int(input('Type:\n1 for text\n2 for images\nor 3 for both\n \n'))

urls = scraper_functions.initiate_scraper()

if operation == 1:
    scraper_functions.scrape_text(urls)
elif operation == 2:
    scraper_functions.scrape_images(urls)
elif operation == 3:
    scraper_functions.scrape_text_and_images(urls)
else:
    print('''I'm sorry, I don't understand! Please select an option from the choices.''')
    operation = input('Type:\n1 for text\n2 for images\nor 3 for both\n \n')
    
print('Program complete!')