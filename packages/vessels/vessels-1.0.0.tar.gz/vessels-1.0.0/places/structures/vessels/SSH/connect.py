



'''
	import vessels.SSH.connect as SSH_connect

	from os.path import dirname, join, normpath
	import pathlib
	import sys

	this_directory = pathlib.Path (__file__).parent.resolve ()
	private_key_path = normpath (join (this_directory, "private key"))

	SSH_connect.splendidly ({
		"private key": "",
		"to": {
			"address": "164.92.112.195"
		}
	})
'''

import os

def splendidly (parameters):
	private_key = parameters ["private key"]
	to_address = parameters ["to"] ["address"]

	script = " ".join ([
		"ssh -i",
		f"'{ private_key }'",
		f"root@{ to_address }"
	])

	print (script);
	
	os.system (script)


