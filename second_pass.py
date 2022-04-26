import os.path
from cache import *
from cached_downloader import *

from bs4 import BeautifulSoup
import json
import urllib.parse
import glob
import csv

models = glob.glob('links/*.model.csv')
print(models)
for model in models:
    with open(model, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        print('opened reader')
        for row in reader:
            print(row)