
'''
	priorities:		
		https://pypi.org/project/simple-term-menu/
'''

import os
from os.path import dirname, join, normpath

def clique ():
	import click
	@click.group ()
	def group ():
		pass
	
	
	import click
	@click.command ("shares")
	def shares ():
		import pathlib
		from os.path import dirname, join, normpath
		this_folder = pathlib.Path (__file__).parent.resolve ()

		import shares
		shares.start ({
			"directory": str (this_folder),
			"extension": ".s.HTML",
			"relative path": str (this_folder)
		})
	group.add_command (shares)
	
	'''
		fleet flask-gunicorn-start --port 
	'''
	import click
	@click.command ("flask-gunicorn-start")
	@click.option ('--port')
	@click.option ('--flask-module-path')
	def flask_gunicorn_start (port, flask_module_path):	
		flask_module_path = normpath (join (os.getcwd (), flask_module_path));
	
		import vessels.flask.gunicorn as flask_gunicorn
		flask_gunicorn.start (
			flask_module_path = flask_module_path
		)
		
	group.add_command (flask_gunicorn_start)

	import click
	@click.command ("flask-gunicorn-stop")
	def flask_gunicorn_stop ():	
		import vessels.flask.gunicorn.stop as stop_flask_gunicorn
		stop_flask_gunicorn.solidly ()
	group.add_command (flask_gunicorn_stop)


	import click
	@click.command ("HA-install-on-fedora")
	def HA_install_on_fedora ():	
		import vessels.proxies.HA.install.Fedora as install_HA_proxy
		install_HA_proxy.charismatically ()
	group.add_command (HA_install_on_fedora)

	import click
	@click.command ("HA-build-papers")
	def build_papers ():	
		import vessels.proxies.HA.SSL as HA_SSL
		HA_SSL.build_papers (
			certificate_path = "/etc/haproxy/SSL/certificate.pem",
			key_path = "/etc/haproxy/SSL/certificate.pem.key"
		)
	group.add_command (build_papers)

	import click
	@click.command ("HA-HTTPS-HTTP")
	@click.option ('--to-port')
	@click.option ('--workers', default = 4)
	def HA_HTTPS_HTTP (to_port, workers):	
		workers = int (workers)
		
		to_addresses = []
		s = 1
		while (s <= workers):
			to_addresses.append (f"0.0.0.0:{ to_port }")
			s += 1

		import vessels.proxies.HA.configs.HTTPS_to_HTTP as HA_HTTPS_to_HTTP
		HA_HTTPS_to_HTTP.build (
			start = "yes",

			SSL_certificate_path = "/etc/haproxy/SSL/certificate.pem",
			config_path = "/etc/haproxy/haproxy.cfg",
			
			to_addresses = to_addresses
		)
	group.add_command (HA_HTTPS_HTTP)

	group ()