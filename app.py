from peewee import *
import csv
from datetime import datetime
from collections import OrderedDict
import os


"""
Helpful documentation around Peewee ORM and retrieving data:  http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#retrieving-data
Other links:
"""


db = SqliteDatabase('inventory.db')


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
    print(" - This app lets you view a database full of store inventory items, and allows you to update as needed")
    print(' - To begin, view the options below and enter the appropriate letter to make a selection (then press enter)')
    print('**********************************************************************************************************')


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
            Product.create(product_name=row['product_name'],
                           timestamp=row['date_updated'],
                           product_quantity=row['product_quantity'],
                           product_price=row['product_price'])

        # myProducts = Product.select().where(Product.product_name.contains('Beans'))

        # practice querying--finding the "Beans"
        # for product in Product.select().where(Product.product_name.contains('Beans')):
            #print(product.product_name)
            #print(product.product_price)


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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('clear')


def add_product():
    """Add a new product"""
    print("you made it into the add product function!!!!!!!!")


def view_product():
    """View the details of a specific product by entering it's ID"""
    choice = input("Enter the product ID you'd like to see details about: ")
    print("ID:     NAME:                                   DATE UPDATED:        QUANTITY:   PRICE:")
    for product in Product.select().where(Product.product_id == choice):
        print_product(product)
    print('\n')

def view_every_product():
    """View EVERY product and their details"""
    print("\nHere are all the products in the database:")
    print("ID:     NAME:                                   DATE UPDATED:        QUANTITY:   PRICE:")
    for product in Product.select():
        print_product(product)
    print('\n')


def backup_products():
    """Creates a backup of entire database to a csv file"""
    print("you made it into the backup product function!!!!!!!")


def print_product(product):
    print(str(product.product_id) +
          (' ' * (8 - len(str(product.product_id)))) +
          product.product_name +
          (' ' * (40 - len(str(product.product_name)))) +
          str(product.timestamp)[:-9] +
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