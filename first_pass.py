from cached_downloader import *
from bs4 import BeautifulSoup

import json
import urllib.parse
import os
import os.path

def cache_countries():
    download_concurrently(get_countries())

def get_countries():
    soup = BeautifulSoup(cache('https://www.tp-link.com/au/choose-your-location/'), features="html.parser")
    location_elements = soup.find_all('li', {'class': 'location-item'})
    #TODO: this only grabs the first a in the li, which is OK for now
    elements = [li.find('a')['href'] + "support/gpl-code/" for li in location_elements]
    return set(elements)

def parse_gpl_list():
    for c in get_countries():
        page = BeautifulSoup(cache(c), features="html.parser")
        
        appPath = page.find('meta', {'name': 'AppPath'}) #used to construct e.g. #https://www.tp-link.com/phppage/gpl-res-list.html?model=Deco%20M5&appPath=kz
        #TODO: We've got "301 Redirect" HTML in our cache, deal with it for now
        if (appPath is None):
            print(f"skipping {c}, was probably a redirect")
            continue
        appPath = appPath['value']

        scripts = page.find_all('script')
        #excludes sites we got a redirect for - e.g. Israel redirects to the generic English page
        results = [s.text for s in scripts if len(s.text) > 0 and 'productTree' in s.text]
        if len(results) == 0:
            return
        results = results[0]
        json_junk_array = results.split('var productTree =')
        for potential_json in json_junk_array:
            potential_json = potential_json.strip()
            if (len(potential_json) and potential_json[0] == '{'): 
                #In the inline script there's another variable we're not interested in
                potential_json = potential_json.split(';\r\n')[0]
                if 'menuTree' in potential_json: #did linebreaks change halfway through the download here?
                    potential_json = potential_json.split(';\n')[0]

def parse_json_product_list(json_string, url, appPath):
    if (os.path.isfile(f'links/{appPath}.tars.csv')):
        return #already done
    tar_links = open(f'links/{appPath}.tars.csv','a')
    model_links = open(f'links/{appPath}.model.csv','a')
    json_file = open(f'links/{appPath}.json','w')
    product_list = json.loads(json_string)
    json_file.write(json_string)
    tar_links.write('link,original_url,model_name,appPath\n')
    model_links.write('link,original_url,model_name,appPath\n')
    #TODO: these variable names are bad
    for model in product_list.items():
        for product in model[1]:
            href = product['href'].strip()
            if '?model' in href:
                model_name = href.split('=')[1]
                model_links.write(f"https://www.tp-link.com/phppage/gpl-res-list.html?model={urllib.parse.quote(model_name)}&appPath={appPath},{url},{product['model_name']},{appPath}\n")
            if not '?model' in href: #direct link to archive, but we can't match on tar as there are zips and rars in places
                tar_links.write(f"{href},{url},{product['model_name']},{appPath}\n")


    tar_links.close()
    model_links.close()
    json_file.close()

if __name__ == '__main__':
    if not os.path.isdir('links'): os.mkdir('links')
    if not os.path.isdir('output'): os.mkdir('output')
    cache_countries()
    parse_gpl_list()