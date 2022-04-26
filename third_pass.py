import glob
import csv

models = glob.glob('links/*.tars.csv')
urls = []
for model in models:
    with open(model, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader, None)
        current_list = [rows[0] for rows in reader]
        urls.extend(current_list)


print(f'{len(urls)} links to tar files, deduplicated it\'s {len(set(urls))}')
#wow, python
#https://stackoverflow.com/a/50223435/229631
with open('urls.txt','w',newline="\n") as download_list:
    download_list.writelines(u + '\n' for u in set(urls))