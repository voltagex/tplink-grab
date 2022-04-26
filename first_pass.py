import os.path
from cache import *
from bs4 import BeautifulSoup
import json
import urllib.parse

def get_countries():
    soup = cache_and_return_bs('https://www.tp-link.com/au/choose-your-location/')
    location_elements = soup.find_all('li', {'class': 'location-item'})
    #TODO: this only grabs the first a in the li, which is OK for now
    elements = [li.find('a')['href'] + "support/gpl-code/" for li in location_elements]
    return set(elements)

def parse_gpl_list():
    for c in get_countries():
        page = cache_and_return_bs(c)
        
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
                parse_json_product_list(potential_json, c, appPath)

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
            href = product['href']
            if '.tar' in href: #direct link to archive
                tar_links.write(f"{href},{url},{product['model_name']},{appPath}\n")
            if '?model' in href:
                model_name = href.split('=')[1]
                model_links.write(f"https://www.tp-link.com/phppage/gpl-res-list.html?model={urllib.parse.quote(model_name)}&appPath={appPath},{url},{product['model_name']},{appPath}\n")

    tar_links.close()
    model_links.close()
    json_file.close()

if __name__ == '__main__':
    parse_gpl_list()



    #TODO: put this back in as a method so people can reproduce my work
    # #https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # # Start the load operations and mark each future with its URL
    #     future_to_url = {executor.submit(cache_and_return_bs, f"{url}support/gpl-code/"): url for url in c}
    #     for future in concurrent.futures.as_completed(future_to_url):
    #         url = future_to_url[future]
    #         try:
    #             data = future.result()
    #         except Exception as exc:
    #             print('%r generated an exception: %s' % (url, exc))
    #         else:
    #             print('%r page is %d bytes' % (url, len(data)))
