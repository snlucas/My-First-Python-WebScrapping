# coding: utf8

# The code below searches for an iPhone on Amazon BR.
# After it finds the product, it'll get the title and 
# name of each product in the first page.
# Then a product table is created for output purposes.
# The output is a CSV file.

from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector
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
    writer.writerow(['Produto', 'Preço'])
    writer.writerows(product_rows)


# Save data as DB
# db-settings file just have two lines
# the first one is the username
# the last one is the password
with open('db-settings.txt', 'r') as db_file:
    db_user = db_file.readline()
    db_password = db_file.readline()

    # or use it:
    # from getpass import getpass
    # db_user = input('DB User: ')
    # db_password = getpass('DB Password: ')

try:
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = db_user,
        password = db_password,
        database = 'amz_db' # created using mariadb/mysql server
    )
except Error as e:
    print(e)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS product (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price VARCHAR(255))")

mycursor.execute("SELECT * FROM product") # catching all the data

product_db = mycursor.fetchall()

if len(product_db) > 0:
    ### Seeking for updates ###
    for i in range(len(iphone['title'])):
        if iphone['price'][i] != product_db[i][-1]:
            sql = "UPDATE product SET name = %s, price = %s WHERE id = %s"
            val = (f"{iphone['title'][i]}", f"{iphone['price'][i]}", str(product_db[i][0]))
            
            mycursor.execute(sql, val)
            mydb.commit()
    ### ### ### ### ### ### ### ### ### ### ### ### ### ###
else:
    # Add products from scratch
    for i in range(len(iphone['title'])):
        product_name = iphone['title'][i]
        product_price = iphone['price'][i]

        sql = "INSERT INTO product (name, price) VALUES (%s, %s)"
        val = [(f'{product_name}', f'{product_price}')]

        mycursor.executemany(sql, val)
        mydb.commit()

print(f'...Finished.\nYour product table was saved as {csv_file_name}\n')
