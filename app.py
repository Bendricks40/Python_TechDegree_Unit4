from peewee import *
import csv
from datetime import datetime
from collections import OrderedDict
import sys
import os


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


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    timestamp = DateTimeField()
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()

    class Meta:
        database = db

