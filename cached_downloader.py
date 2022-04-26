import concurrent.futures
import os.path
import hashlib
from warcio.capture_http import capture_http
from warcio.archiveiterator import ArchiveIterator
from warcio import WARCWriter
import requests #https://github.com/webrecorder/warcio#writing-warc-records

OUTPUT_PATH = 'output/'

#TODO: don't run parsing unless needed
def cache(url):
    if url_already_retrieved(url):
        print(f'Getting {url} from cache')
        return get_from_cache(url)
    
    #https://github.com/webrecorder/warcio/issues/143
    with capture_http(warc_version='1.1') as memory_writer:
        #TODO: do we want to try to append to a single file?
        requests.get(url)

        #TODO: don't run this twice
        fh = open(get_output_filename(url),'wb')
        warc_writer = WARCWriter(fh)
        for record in ArchiveIterator(memory_writer.get_stream()):
            warc_writer.write_record(record)
        fh.close()

        try:
            for record in ArchiveIterator(memory_writer.get_stream()):
                if record.rec_type == 'response':
                    return record.content_stream()
        except:
            raise Exception('aaaa')

def get_output_filename(url):
    return OUTPUT_PATH + hashlib.sha256(url.encode()).hexdigest()

def get_from_cache(url):
    with open(get_output_filename(url),'rb') as reader:
        for record in ArchiveIterator(reader):
            if record.rec_type == 'response' and record.rec_headers.get_header('WARC-Target-URI') == url:
                return record.content_stream().read()
                #TODO: why does this sometimes fail without the .read()? "read on a closed file"
        raise Exception(f"{url} not found in {get_output_filename(url)}")


def url_already_retrieved(url):
    return os.path.isfile(get_output_filename(url))

def download_concurrently(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(cache, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
