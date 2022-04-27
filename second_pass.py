import os.path
from cached_downloader import *

from bs4 import BeautifulSoup
import json
import urllib.parse
import glob
import csv
import random
import logging

logging.basicConfig(level=logging.DEBUG)
models = glob.glob('links/*.model.csv')
urls = []
for model in models:
    with open(model, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader, None)
        current_list = [rows[0] for rows in reader]
        urls.extend(current_list)

download_concurrently(set(urls)) #This will download over 4000 URLs

#drop duplicates
urls = set(urls)


#TODO: this writes duplicates again!
for url in urls:
    write_header = False
    page = BeautifulSoup(cache(url), features="html.parser")
    a = page.find_all('a',href=True)
    query = url.split("?")
    model = query[1].split("=")[1].split("&")[0]
    appPath = query[1].split("=")[2].split("&")[0]
    logging.log(logging.DEBUG,"Processing additional links for %r %r", model, appPath)
    if not os.path.exists(f'links/{appPath}.tars.csv'):
        write_header = True
    with open(f'links/{appPath}.tars.csv', 'a') as tar_list:
        if write_header:
            tar_list.write('link,original_url,model_name,appPath\n')
        for link in a:
            tar_list.write(f"{link['href'].strip()},{url},{model},{appPath}\n")
        