

'''
	import vessels.flask.gunicorn.stop as stop_flask_gunicorn
	stop_flask_gunicorn.solidly (
		PID_file_path = ""
	)
'''


import vessels.flask.gunicorn.process_ID_path as read_process_ID_path
import vessels.flask.gunicorn.settings as flask_gunicorn_settings
	

import os
from os.path import dirname, join, normpath
import pathlib
import psutil
import sys
	
def solidly (
	PID_file_path = ""
):
	if (len (PID_file_path) == 0):
		settings = flask_gunicorn_settings.retrieve ()
		PID_file_name = settings ["PID file name"]
	
		PID_file_path = normpath (join (os.getcwd (), PID_file_name));

	assert (type (PID_file_path) == str)
	assert (len (PID_file_path) >= 1)

	process_ID = int (
		read_process_ID_path.enthusiastically (
			trail = PID_file_path
		)
	)

	p = psutil.Process (process_ID)
	p.terminate ()  #or p.kill()
	
	print ("p:", p)