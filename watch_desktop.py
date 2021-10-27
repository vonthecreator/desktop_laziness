
# HOW TO USE & HOW IT WORKS
# When the script is initiated it listens for changes 
# If any file is modified or touch then the watchdog program will 
# run the appropriate sub-routines to mirror both folders
# move_files.py SRC DEST


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler

import os 
import logging
import json
import time
import sys


class MyHandler(FileSystemEventHandler): 
	def on_modified(self, event):
		for filename in os.listdir(src_folder):
			src = src_folder + "/" + filename
			dest = dest_folder + "/" + filename
			if filename != collection_name:
				os.rename(src, dest) #move file(s)


				



username = sys.argv[1] #parse param1 (source folder) from CLI
collection_name = sys.argv[2] #parse param2 (destination folder) from CLI
src_folder = "/Users/"+username+"/Desktop"
dest_folder = "/Users/"+username+"/Desktop/"+collection_name
event_handler = MyHandler()
event_logger = LoggingEventHandler()

## log changes
logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')

observer = Observer()
observer.schedule(event_handler, src_folder, recursive = True)
observer.start() #start monitoring changes



try: 
	while True:
		time.sleep(10)
except KeyboardInterrupt: #unless I hit ctr-c


	observer.stop()
	observer.join()
