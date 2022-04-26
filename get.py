import os.path
import hashlib

from warcio.capture_http import capture_http
from warcio.archiveiterator import ArchiveIterator
import requests #https://github.com/webrecorder/warcio#writing-warc-records
from bs4 import BeautifulSoup

#https://gist.github.com/edsu/62bc39890806ffd19b597186a3619419

OUTPUT_PATH = 'output/'

def cache_and_return_bs(url):
    if url_already_retrieved(url):
        raise Exception(url + ' already there')
    
    #https://github.com/webrecorder/warcio/issues/143
    with capture_http(warc_version='1.1') as memory_writer:
        #TODO: do we want to try to append to a single file?
        requests.get(url)

        #TODO: don't run this twice
        file_writer = open(get_output_filename(url),'wb')
        for record in ArchiveIterator(memory_writer.get_stream()):
            file_writer.write_record(record)
        file_writer.close()

        for record in ArchiveIterator(memory_writer.get_stream()):
            if record.rec_type == 'response':
                return BeautifulSoup(record.content_stream())

def get_output_filename(url):
    return OUTPUT_PATH + hashlib.sha256(url.encode()).hexdigest()

def url_already_retrieved(url):
    return os.path.isfile(get_output_filename(url))


if __name__ == '__main__':
    print(cache_and_return_bs('https://www.tp-link.com/au/choose-your-location/'))