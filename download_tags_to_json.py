# https://www.instagram.com/explore/tags/test/
import argparse
import sys
import os
import httplib
import urlparse
import json
import threading
import Queue
import math

parser = argparse.ArgumentParser(description='Instagram Popular Tags')
parser.add_argument('-s', '--source', type=argparse.FileType('r'), help='the list of words', nargs='?', default=sys.stdin)

args = parser.parse_args()

if args.source:

    concurrent = 10

    def create_worker():
        while True:
            worker_data = q.get()
            worker_parsed_url = urlparse.urlparse(worker_data['remote_url'])
            data = read_response(worker_data['remote_url'], worker_parsed_url)
            if data:
                write_to_json(data, worker_data['word'])
            q.task_done()

    def read_response(workerurl, read_parsed_url):
        try:
            conn = httplib.HTTPSConnection(read_parsed_url.netloc)
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Accept": "text/html",
                "accept-language": "en-US"
            }
            conn.request('GET', read_parsed_url.path, headers=headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()
            if 'OK' in res.reason:
                if len(data) > 0:
                    return data
            else:
                print "Error with reason: " + str(res.status) + " in url: %s" % workerurl
            return False
        except (httplib.HTTPException) as e:
            print "Something went wrong with url: %s" % e
            return False

    def write_to_json(response_data, word):
        if response_data:
            myfile = 'wordpages/' + word + '.json'
            if not os.path.isfile(myfile):
                # strip response data
                strip1 = response_data.split(r'window._sharedData = ')
                if len(strip1) > 1:
                    strip2 = strip1[1].split(r";</script>")
                    if len(strip2) > 0:
                        with open(myfile, "w") as outfile:
                            # write json to directory
                            print "\nDownloading instagram hashtag: %s" % word
                            outfile.write(strip2[0])
                            return True
        return False

    q = Queue.Queue(concurrent * 2)
    for i in range(concurrent):
        t = threading.Thread(target=create_worker)
        t.daemon = True
        t.start()
    try:
        for word in args.source:
            url = 'https://www.instagram.com/explore/tags/'+ word.strip().lower() + '/'
            data = {
                'remote_url': url,
                'word': word.strip().lower()
            }
            q.put(data)
        q.join()

    except KeyboardInterrupt:
        sys.exit(1)
