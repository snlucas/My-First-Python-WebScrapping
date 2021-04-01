
# Searching for an item on Amazon Brazil

from bs4 import BeautifulSoup
import requests


# iPhone is the item we are looking for
iphone = { 'title':[], 'price':[] }
query_item = 'iphone'
url = f'https://www.amazon.com.br/s?k={query_item}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'

content = requests.get(url)
soup = BeautifulSoup(content.text, 'lxml')

content = soup.find_all('div', class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20')  # Get data from a higher parent that wraps the itens in the page
itens = [item.find('div', class_='a-section a-spacing-medium') for item in content]  # Get data from the content variable and look closely for the card element that has the info about the product

# Get product info
item_name = [item.find('span', class_='a-size-base-plus a-color-base a-text-normal') for item in itens]
item_price = [item.find('span', class_='a-price') for item in itens]

# Populate iphone dictionary
iphone['title'] = [name.text for name in item_name]
for item in itens:
    # Product without a price doesnt have a tag span with a class a-price. Therefore, we need to deal with a possible search for a non-existent tag
    try:
        iphone['price'].append(item.find('span', class_='a-price').find('span', class_='a-offscreen').text)
    except AttributeError:
        iphone['price'].append('No price')  # If we find some non-exitent tag, we need to put some data in the list. Otherwise, we may have some ignored data that will be a problem when we need to show results in a grouped way 

print(f"Len Title: {len(iphone['title'])},\nLen Price: {len(iphone['price'])}")