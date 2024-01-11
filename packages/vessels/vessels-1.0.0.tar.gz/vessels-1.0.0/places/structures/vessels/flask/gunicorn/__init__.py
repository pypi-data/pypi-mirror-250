from __future__ import print_function

'''
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	PID_file_path = normpath (join (this_directory, "gunicorn.process_ID"))

	import vessels.flask.gunicorn as flask_gunicorn
	flask_gunicorn.start (
		flask_module_path = "",
		port = 54031,
		workers = 4
	)
'''

'''
	flask_gunicorn.start (
		PID_file_path = PID_file_path,
		flask_def = start,
		port = 54031,
		workers = 4
	)
'''


import builtins

import os
from os.path import dirname, join, normpath

import vessels.flask.gunicorn.settings as flask_gunicorn_settings
import vessels.flask.gunicorn.import_custom as import_custom
	
def start (
	PID_file_path = "",
	flask_module_path = "",

	workers = 4,
	port = 54031
):
	if (len (PID_file_path) == 0):
		settings = flask_gunicorn_settings.retrieve ()
		PID_file_name = settings ["PID file name"]
	
		PID_file_path = normpath (join (os.getcwd (), PID_file_name));

	#assert (type (flask_module_path) == str)
	#assert (len (flask_module_path) >= 1)
	
	assert (len (PID_file_path) >= 1)

	print (
		PID_file_path,
		flask_module_path,

		workers,
		port
	)
	
	flask_module = import_custom.start (flask_module_path);
	
	from gunicorn.app.base import Application
	class FlaskApplication (Application):
		def init (self, parser, opts, args):
			#
			#	This is run in another process presumably
			#
		
			return {			
				'bind': f'0.0.0.0:{ port }',
				'workers': int (workers),
				
				'daemon': True,
				'pidfile': PID_file_path
			}

		def load (self):
			#
			#	This is run in another process presumably
			#
		
			#return flask_module_path ()
			return flask_module.start ()

	print ('gunicorn is starting')

	application = FlaskApplication ()
	application.run ()
