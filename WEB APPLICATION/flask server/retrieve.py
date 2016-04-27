import json
from pprint import pprint

with open('result.json') as data_file:    
    data = json.load(data_file)
data_file.close()
x = raw_input("enter infoid")
y=0
while y<2:
	z = data[y]['infoid']
	if int(z)==int(x):
		print pprint(data[y]['fname'])
	y=y+1

