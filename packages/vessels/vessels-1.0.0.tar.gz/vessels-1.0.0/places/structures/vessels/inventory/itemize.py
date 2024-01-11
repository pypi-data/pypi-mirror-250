
'''
import vessels.inventory.itemize as itemize_inventory
itemize_inventory.start ()
'''

import glob
import json

def start (directories):
	inventory = {}

	for directory in directories:
		inventory_glob_string = folder + "/**/*"
		inventory_paths = glob.glob (folder + "/**/*", recursive = True)
		
		for path in inventory_paths:
			inventory [ path.split (folder + "/") [1] ] = path;
		
	print ("inventory:", json.dumps (inventory, indent = 4))
		
	return inventory