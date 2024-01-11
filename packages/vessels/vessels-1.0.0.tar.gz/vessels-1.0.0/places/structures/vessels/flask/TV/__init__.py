


'''

'''


def start ():
	from flask import Flask

	app = Flask (__name__)

	@app.route ("/")
	def hello ():
		return "$"
		
	@app.route ('/', defaults={'path': ''})
	@app.route ('/<path:path>')
	def catch_all (path):
		return 'You want path: %s' % path
		
	return app;
	



