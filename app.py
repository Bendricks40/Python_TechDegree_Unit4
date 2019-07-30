from peewee import *
import csv
import datetime
from datetime import datetime
from collections import OrderedDict
import os


"""
Helpful documentation around Peewee ORM and retrieving data:  
http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#retrieving-data
Other links: 
https://stackoverflow.com/questions/41915140/delete-the-contents-of-a-file-before-writing-to-it-in-python/41915206
"""


db = SqliteDatabase('inventory.db')
header = "ID:     NAME:                                   DATE UPDATED:        QUANTITY:   PRICE:"


class Product(Model):
    product_id = AutoField()
    timestamp = DateTimeField()
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()

    class Meta:
        database = db


def welcome():
    print('\n')
    print("**************************************  Welcome to Store Inventory!  *************************************")
    print(" * This app lets you view a database full of store inventory items, and allows you to update as needed")
    print(" * Created by Ben Hendricks as part of TeamTreehouse's Python TechDegree, Unit 4")
    print(" * To begin, view the options below and enter the appropriate letter to make a selection (then press enter)")
    print("**********************************************************************************************************")


def initialize():
    """create table and db"""
    db.connect()
    # print("Just connected to DB")
    db.create_tables([Product], safe=True)
    # print("just created tables")


def open_and_clean_csv():
    with open('inventory.csv', newline='') as csvfile:
        artreader = csv.DictReader(csvfile, delimiter=',')
        rows = list(artreader)
        for row in rows[:]:

            # store product quantity as an int vs string
            row['product_quantity'] = int(row['product_quantity'])

            # then take product price and strip out the dollar sign and period
            row['product_price'] = (row['product_price'].strip('$')).replace('.', '')

            # once price is just cents (but still a string), convert it to an int:
            row['product_price'] = int(row['product_price'])

            # change the date updated value to be stored as a date:
            row['date_updated'] = datetime.strptime(row['date_updated'], '%m/%d/%Y')

            # now add the item to the database:
            if Product.select().where(Product.product_name.contains(row['product_name'])):
                # print("The product '{}' already exists. Checking if this is "
                # "a newer version...".format(row['product_name']))
                for product in Product.select().where(Product.product_name.contains(row['product_name'])):
                    # print('The existing timestamp for this item is: {}, and the '
                    # 'item we are trying to insert has a timestamp '
                    # 'of {}'.format(product.timestamp, row['date_updated']))
                    if product.timestamp < row['date_updated']:
                        # print('Looks like we have a newer timestamp! Time to '
                        # 'update the quantity/price/timestamp with this new info')
                        product.timestamp = row['date_updated']
                        product.product_quantity = row['product_quantity']
                        product.product_price = row['product_price']
                        product.save()
                    else:
                        pass
                        # print("this is NOT a newer timestamp, so nothing to do here.")
            else:
                Product.create(product_name=row['product_name'],
                               timestamp=row['date_updated'],
                               product_quantity=row['product_quantity'],
                               product_price=row['product_price'])


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Choose an option below, or press 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        else:
            print("Oops, that wasn't a valid selection. Try again...\n")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('clear')


def add_product():
    """Add a new product"""
    newProduct_name = input("Enter a name for the new product: ")
    validPrice = False
    validQuantity = False

    while not validQuantity:
        try:
            newProduct_quantity = int(input("Enter total available quantity for this product: "))
            validQuantity = True
        except ValueError:
            print("Not a valid quantity, try again!")

    while not validPrice:
        try:
            newProduct_price = int(input('Enter a price for the product in pennies--i.e. '
                                         '$3.44 would be entered as 344 (no dollar sign needed): '))
            validPrice = True
        except ValueError:
            print("Not a valid price, try again!")

    if validPrice and validQuantity:
        if Product.select().where(Product.product_name == newProduct_name):
            for product in Product.select().where(Product.product_name == newProduct_name):
                product.timestamp = datetime.now().strftime('%Y-%m-%d')
                product.product_quantity = newProduct_quantity
                product.product_price = newProduct_price
                product.save()
                print("\nThis product already existed, but we took your newer data "
                      "and saved it so that now '{}' has been updated successfully!\n\n".format(newProduct_name))
        else:
            Product.create(product_name=newProduct_name,
                           timestamp=datetime.now().strftime('%Y-%m-%d'),
                           product_quantity=int(newProduct_quantity),
                           product_price=int(newProduct_price))
            print("\n'{}' has been successfully added to the database!\n\n".format(newProduct_name))


def view_product():
    """View the details of a specific product by entering it's ID"""
    exists = False
    while not exists:

        try:
            choice = int(input("Enter the product ID you'd like to see details about: "))
            for product in Product.select().where(Product.product_id == choice):
                exists = True
                print(header)
                print_product(product)
                break
            else:
                print("That ID doesn't exist...try again!")
            print('\n')

        except ValueError:
            print("Oops, that wasn't a valid number. Try again with a numeric ID")


def view_every_product():
    """View EVERY product and their details"""
    print("\nHere are all the products in the database:")
    print(header)
    for product in Product.select():
        print_product(product)
    print('\n')


def backup_products():
    """Creates a backup of entire database to a csv file"""
    with open('backup.csv', 'a') as csvfile:
        # Clear out existing file contents, if any
        csvfile.seek(0)
        csvfile.truncate()
        # Now write the new stuff into the file by first creating the header names:
        fieldnames = ['product_id', 'product_name', 'product_timestamp', 'product_quantity', 'product_price']
        # Create the actual CSV writer object:
        productWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Throw a good ol' header in there:
        productWriter.writeheader()
        # Now walk through each product and write it as a line into the file:
        for product in Product.select():
            productWriter.writerow({'product_id': product.product_id,
                                    'product_name': product.product_name,
                                    'product_timestamp': product.timestamp,
                                    'product_quantity': product.product_quantity,
                                    'product_price': product.product_price})
    # Close out the file:
    csvfile.close()
    print("\nBackup has been created entitled 'backup.csv'\n\n")


def print_product(product):
    print(str(product.product_id) +
          (' ' * (8 - len(str(product.product_id)))) +
          product.product_name +
          (' ' * (40 - len(str(product.product_name)))) +
          str(product.timestamp)[:10] +
          (' ' * (30 - len(str(product.timestamp)))) +
          str(product.product_quantity) +
          (' ' * (12 - len(str(product.product_quantity)))) +
          '$' + str(product.product_price / 100))


menu = OrderedDict([
    ('a', add_product),
    ('v', view_product),
    ('b', backup_products),
    ('e', view_every_product)
])


if __name__ == '__main__':
    welcome()
    initialize()
    open_and_clean_csv()
    menu_loop()