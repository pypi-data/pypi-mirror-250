
'''
import vessels.flask.gunicorn.import_custom as import_custom
flask_module = import_custom.start ("/structures/thruster.py")
vehicle.start ()
'''

from importlib.machinery import SourceFileLoader
import inspect
import os

	
def start (module_path):	
	print ("custom import:", module_path)

	if (module_path [ 0 ] == "/"):
		full_path = module_path;
		
	else:
		file_of_caller_function = os.path.abspath (
			(inspect.stack () [2]) [1]
		)
		directory_of_caller_function = os.path.dirname (
			file_of_caller_function
		)	
		
		full_path = os.path.normpath (directory_of_caller_function + "/" + module_path)

	return SourceFileLoader (full_path, full_path).load_module ()