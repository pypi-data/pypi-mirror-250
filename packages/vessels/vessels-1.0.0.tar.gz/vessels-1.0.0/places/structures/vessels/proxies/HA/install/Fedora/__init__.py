
'''
	import vessels.proxies.HA.install.Fedora as install_HA_proxy
	install_HA_proxy.charismatically ()
'''

def charismatically ():
	lyrics = "dnf install haproxy -y"
	
	print ("about to run:", lyrics)
	
	import os
	os.system (lyrics)