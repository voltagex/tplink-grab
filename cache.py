OUTPUT_PATH = 'output/'
import os.path
import hashlib
from warcio.capture_http import capture_http
from warcio.archiveiterator import ArchiveIterator
from warcio import WARCWriter
import requests #https://github.com/webrecorder/warcio#writing-warc-records
from bs4 import BeautifulSoup

#TODO: don't run parsing unless needed
def cache_and_return_bs(url):
    if url_already_retrieved(url):
        #print(f'Getting {url} from cache')
        return get_bs_from_cache(url)
    
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

        for record in ArchiveIterator(memory_writer.get_stream()):
            if record.rec_type == 'response':
                return BeautifulSoup(record.content_stream(), features="html.parser")

def get_output_filename(url):
    return OUTPUT_PATH + hashlib.sha256(url.encode()).hexdigest()

def get_bs_from_cache(url):
    with open(get_output_filename(url),'rb') as reader:
        for record in ArchiveIterator(reader):
            if record.rec_type == 'response' and record.rec_headers.get_header('WARC-Target-URI') == url:
                return BeautifulSoup(record.content_stream(), features="html.parser")
        raise Exception(f"{url} not found in {get_output_filename(url)}")

def url_already_retrieved(url):
    return os.path.isfile(get_output_filename(url))

