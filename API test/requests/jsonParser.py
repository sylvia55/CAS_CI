import json

file = open('.\config.json', 'r')
data = json.load(file)
file.close()
def loadParameter(name):
	content = data[name]
	for k,v in content:
	

loadParameter('clone')
loadParameter('delete')