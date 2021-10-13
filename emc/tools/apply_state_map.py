import csv, PIL, math
from PIL import Image
from pathlib import Path
import re
# Generate states

# References to provinces in the game files
rgx = re.compile("id *= *([0-9]+)[ \t#\n]")
province_references = {}
province_referenced_where = {}
province_colors = {}
color_provinces = {}
province_sizes ={}
province_extra_data = {}
state_colors = {}
states = {}

maxid = 0

from math import sqrt, floor
PHI = (1 + sqrt(5))/2
def nth_color(n):
	n = n * PHI - floor(n * PHI)
	return (floor(n * 256), floor(n * 256 ** 2) % 256, floor(n * 256 ** 3) % 256)

def data_to_file(data):
	(start, provinces, end) = data
	return start + "provinces = { \n" + " ".join(str(i) for i in provinces) + "\n}\n" + end
	
def add_file(filename):
	global province_references
	global maxid
	with open(filename) as f:
		data = f.read()
		m = re.match("(.+?)provinces[ \n\t]*=[ \n\t]*{(.+?)}(.+)$", data, flags=re.DOTALL)
		assert m != None
		provinces = [int(i) for i in m.group(2).strip().split(" ") if i.strip()]
		l = [m.group(1), provinces, m.group(3)]
		sid = int(rgx.search(l[0]).group(1))
		states[sid] = l
		maxid = max(maxid, sid)
		province_references[filename] = l
		for i in provinces:
			if province_referenced_where.get(i) == None:
				province_referenced_where[i] = []
			province_referenced_where[i].append(l)

added_colors = set()
for i in range(1000):
	assert nth_color(i) not in added_colors
	added_colors.add(nth_color(i))
	

for i in Path("history/old_states").iterdir():
	add_file(i)

import itertools	

im = Image.open('map/provinces.bmp')
state_map = Image.open("state_map.png")

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

assert 905 in states
	
# Remove gaps in province definition
max_id = max(list(province_colors.keys()))
for idx in range(1,max_id+1):
	if province_colors.get(idx) == None:
		# Scan ahead
		for jdx in range(idx, max_id+1):
			if province_colors.get(jdx) != None:
				reassign_province_id(jdx, idx)
				break
				
moved_provinces = set()
first_state_provinces = {}
state_colors = {}
color_states = {}

for x in range(im.width):
	for y in range(im.height):
		color = im.getpixel((x, y))
		province = color_provinces[color]
		if province in moved_provinces:
			continue
		if province_referenced_where.get(province) != None:
			m = rgx.search(province_referenced_where[province][0][0])
			if m:
				state_id = int(m.group(1))
				state_color = state_map.getpixel((x, y))
				if first_state_provinces.get(state_id) == None:
					first_state_provinces[state_id] = province
				if state_colors.get(state_id) == None:
					state_colors[state_id] = state_color
					color_states[state_color] = state_id
				
				if state_colors[state_id] != state_color:
					# New state
					province_referenced_where[province][0][1].remove(province)
					if color_states.get(state_color) == None:
						new_state_id = maxid + 1
						while new_state_id in states:
							new_state_id += 1
						maxid = max(maxid, new_state_id)
		
						color_states[state_color] = new_state_id
						new_state = [*province_referenced_where[province][0]]
						new_state[1] = []
						new_state[0] = rgx.sub("id = " + str(new_state_id) + "\n", new_state[0])
						states[new_state_id] = new_state
						state_colors[new_state_id] = state_color
						province_references["history/states/" + str(new_state_id) + "-UNK.txt"] = new_state
					else:
						new_state_id = color_states[state_color]
						new_state = states[new_state_id]
						
					new_state[1].append(province)
					print(f"Add {province} to {new_state_id} {state_color}")
					pass
				else:
					pass
				
		moved_provinces.add(province)
					
					
				
				
	#print(x / im.width)
	
for k, v in province_references.items():
	with open(str(k).replace("old_", ""), "w") as f:
		f.write(data_to_file(v))

		
'''	
for k, v in province_references.items():
	with open("new_" + str(k), "w") as f:
		f.write(data_to_file(v))
'''