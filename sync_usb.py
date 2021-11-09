import usb
import psutil
import sys, csv, time, os, logging, json
import sysrsync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler



product_id = "3281"
serial_num = "0303600000000331" #books
dest_folder = '/Volumes/Virus_/git'
src_folder = '/Users/munazhe/Desktop/desktop_laziness/git'
username = 'munazhe' #parse param1 (source folder) from CLI
collection_name = 'desktop_laziness/git' #parse param2 (destination folder) from CLI




class MyHandler(FileSystemEventHandler): 
	def on_modified(self, event):
		for filename in os.listdir(src_folder):
			src = src_folder + "/" + filename
			dest = dest_folder + "/" + filename
			if filename != collection_name and is_pluggedin(serial_num, product_id): 
				time.sleep(30) #run every 30 seconds
				sysrsync.run(source=src_folder,
								destination=dest_folder,
								options=['-avzh'],
								sync_source_contents=True)



def is_pluggedin(serial_num, product_id):
	try:
		for device in usb.core.find(find_all=True):
			if str(serial_num) in str(usb.util.get_string(device, device.iSerialNumber)) and str(product_id) in str(device.idProduct):
				return True

		return False # usb not found
	except BaseException as exception: 
		print(exception)
		return False
pass



event_handler = MyHandler()
event_logger = LoggingEventHandler()
logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')

observer = Observer()
observer.schedule(event_handler, src_folder, recursive = True)
observer.start() #start monitoring changes



try:
	while True:
		time.sleep(10)
except BaseException as error: 
	observer.stop()
	observer.join()
	print(error)
		