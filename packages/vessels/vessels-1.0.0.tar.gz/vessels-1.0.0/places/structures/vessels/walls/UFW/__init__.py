

'''
	priorities:
		import vessels.walls.UFW as UFW
		UFW.start ({
			"out": "yes",
			
			"ports": [{
				"number": 443,
				"protocols": [ "TCP" ],
				
				"out": "yes",
				"in": "yes"
			},{
				"number": 80,
				"protocols": [ "TCP" ],
				
				"out": "yes",
				"in": "yes"
			},{
				"number": 22,
				"protocols": [ "TCP", "UDP" ],
				
				"out": "yes",
				"in": "yes"
			}]
		})
'''

def start ():
	return;