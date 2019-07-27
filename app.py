from peewee import *
import csv
from datetime import datetime
from collections import OrderedDict
import os


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    timestamp = DateTimeField()
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()

    class Meta:
        database = db


def open_and_clean_csv():
    with open('inventory.csv', newline='') as csvfile:
        artreader = csv.DictReader(csvfile, delimiter=',')
        rows = list(artreader)
        for row in rows[1:]:

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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def initialize():
    """create table and db"""
    db.connect()
    print("Just connected to DB")
    db.create_tables([Product], safe=True)
    print("just created tables")


def add_product():
    """Add a new product"""
    print("you made it into the add product function!!!!!!!!")


def view_product():
    """View the details of a specific product"""
    print("you made it into the 'view product' Function!!!!!!!!")


def view_every_product():
    """View EVERY product and their details"""
    print("\nHere are all the products in the database:")
    # to get everything to line up nicely, I used the len of prior
    # value to fit things into same starting position
    print("ID:     NAME:                                   PRICE:  QUANTITY:")
    for product in Product.select():
        print(str(product.product_id) +
              (' '*(8-len(str(product.product_id)))) +
              product.product_name +
              (' '*(40-len(str(product.product_name)))) +
              str(product.product_price) +
              (' '*(8-len(str(product.product_price)))) +
              str(product.product_quantity))
    print('\n')


def backup_products():
    """Creates a backup of entire database to a csv file"""
    print("you made it into the backup product function!!!!!!!")


menu = OrderedDict([
    ('a', add_product),
    ('v', view_product),
    ('b', backup_products),
    ('e', view_every_product)
])


if __name__ == '__main__':
    initialize()
    open_and_clean_csv()
    menu_loop()

