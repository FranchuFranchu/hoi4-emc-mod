import csv, PIL, math
from PIL import Image
from pathlib import Path
import re
# Generate states

# References to provinces in the game files
province_references = {}
province_referenced_where = {}
province_colors = {}
color_provinces = {}
province_sizes ={}
province_extra_data = {}
state_colors = {}


from math import sqrt, floor
PHI = (1 + sqrt(5))/2
def nth_color(n):
	n = n * PHI - floor(n * PHI)
	return (floor(n * 256), floor(n * 256 ** 2) % 256, floor(n * 256 ** 3) % 256)

def add_file(filename):
	global province_references
	with open(filename) as f:
		data = f.read()
		m = re.match("(.+?)provinces[ \n\t]*=[ \n\t]*{(.+?)}(.+)$", data, flags=re.DOTALL)
		assert m != None
		provinces = [int(i) for i in m.group(2).strip().split(" ") if i.strip()]
		l = [m.group(1), provinces, m.group(3)]
		province_references[filename] = l
		for i in provinces:
			if province_referenced_where.get(i) == None:
				province_referenced_where[i] = []
			province_referenced_where[i].append(l)

added_colors = set()
for i in range(1000):
	assert nth_color(i) not in added_colors
	added_colors.add(nth_color(i))
	

for i in Path("history/states").iterdir():
	add_file(i)

import itertools	

im = Image.open('map/provinces.bmp')
state_map = Image.new("RGB", im.size)

with open("map/definition.csv") as fp:
	reader = csv.reader(fp, delimiter=";")

	for i in reader:
		color = tuple(int(i) for i in i[1:4])
		
		id = int(i[0])
		
		color_provinces[color] = id
		province_colors[id] = color
		province_extra_data[id] = i[4:]

for count, color in im.getcolors(100000):
	#print(provs[color], count)
	assert province_colors[color_provinces[color]] == color
	province_sizes[color_provinces[color]] = count


	
# Remove gaps in province definition
max_id = max(list(province_colors.keys()))
for idx in range(1,max_id+1):
	if province_colors.get(idx) == None:
		# Scan ahead
		for jdx in range(idx, max_id+1):
			if province_colors.get(jdx) != None:
				reassign_province_id(jdx, idx)
				break
rgx = re.compile("id=([0-9]+)")
for x in range(im.width):
	for y in range(im.height):
		color = im.getpixel((x, y))
		province = color_provinces[color]
		if province_referenced_where.get(province) != None:
			m = rgx.search(province_referenced_where[province][0][0])
			if m:
				state_id = int(m.group(1))
				state_map.putpixel((x, y), nth_color(state_id))
				
	print(x / im.width)
	
state_map.save("state_map.png")
		
'''	
for k, v in province_references.items():
	with open("new_" + str(k), "w") as f:
		f.write(data_to_file(v))
'''