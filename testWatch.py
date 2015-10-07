import time
import urllib2

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.xml", "*.lxml"]

    def process(self, event, html):
        #event.event_type, event.is_directory True | False, event.src_path
        print html

    def on_modified(self, event):
        response = urllib2.urlopen('http://localhost:8080/save')
        html = response.read()
        self.process(event, html)

    def on_created(self, event):
        response = urllib2.urlopen('http://localhost:8080/save')
        html = response.read()
        self.process(event, html)
		
if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path='./webapp/')
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()