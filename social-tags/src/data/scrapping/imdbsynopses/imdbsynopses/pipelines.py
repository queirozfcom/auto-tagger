# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
from datetime import date

class ImdbsynopsesPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvWriterPipeline(object):

    def __init__(self):
        self.fieldnames = ['imdbId', 'synopsis']

        todays_date = date.today().isoformat()

        self.path_to_output_file = os.path.abspath("../../../../../../data/raw/")+"imdb_synopses-{}.csv".format(todays_date)

    def open_spider(self, spider):
        self.file = open(self.path_to_output_file, 'w')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=self.fieldnames,escapechar='\\',doublequote=False, quoting=csv.QUOTE_ALL)
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(item)
        return item
