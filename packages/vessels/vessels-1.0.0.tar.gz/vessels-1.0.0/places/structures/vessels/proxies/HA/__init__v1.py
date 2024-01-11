





def add_to_system_paths (trails):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	for trail in trails:
		sys.path.insert (0, normpath (join (this_directory, trail)))

add_to_system_paths ([ 
	'structures',
	'structures_pip'
])


import os
import pathlib
from os.path import dirname, join, normpath
import sys
this_directory = pathlib.Path (__file__).parent.resolve ()

config_path = str (normpath (join (this_directory, "haproxy.conf")))
config_path = "/etc/haproxy/haproxy.cfg"


defaults_2 = f'''
defaults
	mode                    http
	log                     global
	option                  httplog
	option                  dontlognull
	option http-server-close
	option forwardfor       except 127.0.0.0/8
	option                  redispatch
	retries                 3
	
	# errorfile 503 /etc/haproxy/errors/503.http
	
	timeout http-request    10s
	timeout queue           1m
	timeout connect         10s
	timeout client          1m
	timeout server          1m
	timeout http-keep-alive 10s
	timeout check           10s
	
	maxconn                 3000
'''

backend = f'''
backend app
	balance leastconn
	#balance roundrobin
	server app10 0.0.0.0:8000 check
	server app20 0.0.0.0:8001 check
'''

backend = f'''
backend app
	server app_10 127.0.0.1:8000 check
'''


defaults = f'''
defaults
	mode http
	timeout connect 5000ms
	timeout client 50000ms
	timeout server 50000ms
'''

config = f"""
global
	chroot /var/lib/haproxy

	daemon
	maxconn 256
	user haproxy
	group haproxy

	# turn on stats unix socket
	# stats socket /var/lib/haproxy/stats

{ defaults }

frontend http-in
	bind *:80
	# mode http
	
	
	default_backend app

{ backend }
"""




import configs.HTTP_balancer as HTTP_balancer_config
config = HTTP_balancer_config.build ({
	"from": "80",
	"to": [
		"0.0.0.0:8000",
		"0.0.0.0:8001"
	]
})

FP = open (config_path, "w")
FP.write (config)
FP.close ()

os.system (f"haproxy -f '{ config_path }' -c")
os.system ("systemctl restart haproxy")
os.system (f"cat '{ config_path }'")
os.system ("systemctl status haproxy -l --no-pager")


#os.system ("haproxy -f haproxy.conf -c")
#os.system ("haproxy -f haproxy.conf")
