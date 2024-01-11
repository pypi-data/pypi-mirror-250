

'''

import vessels
sels = vessels.prevail ({
	"port": "57384",
	"
})

app = sels.app;

@app.route ('/')
def home ():		
	return send_file (home_html)
'''

'''
	priorities:
		gunicorn
		gevent
'''


import vessels.clique as vessels_clique
def clique ():
	print ("vessels clique")
	
	vessels_clique.clique ()

from flask import Flask, request, send_file, request, make_response, send_from_directory, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit

def prevail (parameters):

	app = Flask (__name__)
	
	
	
	app.run (
		port = port
	)

	return;