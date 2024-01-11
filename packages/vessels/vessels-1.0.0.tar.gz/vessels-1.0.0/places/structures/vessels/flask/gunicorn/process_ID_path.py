



'''
import vessels.flask.gunicorn.process_ID_path as read_process_ID_path
read_process_ID_path.enthusiastically ()
'''

'''
def retrieve ():
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	return normpath (join (this_directory, "gunicorn.process_ID"))
'''	
	
import pathlib
from os.path import dirname, join, normpath
import sys


import os

	
import os
def enthusiastically (
	trail = ""
):
	if (os.path.isfile (trail)):
		FP = open (trail, "r")
		return FP.read ().strip ()
		
	else:
		raise Exception ("The gunicorn process ID file was not found.")

	