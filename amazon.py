# The code below searches for an iPhone on Amazon BR.
# After it finds the product, it'll get the title and 
# name of each product in the first page.
# Then a product table is created for output purposes.
# The output is a CSV file.

from bs4 import BeautifulSoup
import requests
import csv
import sys


# iPhone is the item we are looking for
iphone = { 'title':[], 'price':[] }
query_item = 'iphone'
url = f'https://www.amazon.com.br/s?k={query_item}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss' 

# Looking for an OK status code
for i in range(100):
    content = requests.get(url)
    status = content.status_code

    if(status >= 400):
        if(status >= 500):
            print(f'Server error status {status}')
        else:
            print(f'Client error status {status}')
        print('Trying again...')
    else:
        # Show some info for the user and fall out the loop
        print(f'\nfinding for {query_item}...')
        break

    # Program must not continue, because it cannot connect to server.
    if(i == 99):
        print('Cannot connect. Tried to connect to server one hundred times without success.\nTry again later.')
        sys.exit()

soup = BeautifulSoup(content.text, 'lxml')

content = soup.find_all('div', class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20')  # Get data from a higher parent that wraps the itens in the page
itens = [item.find('div', class_='a-section a-spacing-medium') for item in content]  # Get data from the content variable and look closely for the card element that has the info about the product

# Get product info
item_name = [item.find('span', class_='a-size-base-plus a-color-base a-text-normal').text for item in itens]
item_price = [item.find('span', class_='a-price') for item in itens]

# Populate iphone dictionary
iphone['title'] = item_name
for item in item_price:
    # Product without a price doesnt have a tag span with a class a-price. Therefore, we need to deal with a possible search for a non-existent tag
    try:
        iphone['price'].append(item.find('span', class_='a-offscreen').text)
    except AttributeError:
        iphone['price'].append('No price')  # If we find some non-exitent tag, we need to put some data in the list. Otherwise, we may have some ignored data that will be a problem when we need to show results in a grouped way 

# It'll be used as an output table
product_rows = [[iphone['title'][i], iphone['price'][i]] for i in range(len(itens))]

# Save data as a CSV file
csv_file_name = 'amazon_iphone_prices.csv'
with open(csv_file_name, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(product_rows)

print(f'...Finished.\nYour product table was saved as {csv_file_name}\n')
