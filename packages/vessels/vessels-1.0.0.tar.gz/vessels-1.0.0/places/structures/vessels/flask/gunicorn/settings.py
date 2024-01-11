
'''
	import vessels.flask.gunicorn.settings as flask_gunicorn_settings
	settings = flask_gunicorn_settings.retrieve ()
	PID_file_name = settings ["PID file name"]

'''

def retrieve ():
	return {
		"PID file name": "gunicorn.process_ID"
	}