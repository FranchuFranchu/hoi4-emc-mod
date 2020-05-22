# Use this with GIMP
# Copy and paste into the terminal
# Last time i tested it didn't work


def save_mod(filename):
	img = pdb.gimp_file_load(filename, filename)
	img.scale(41,26)
	new_filename = '/'.join(filename.split('/')[0:-1]) + "/medium/" + filename.split('/')[-1]
	pdb.gimp_file_save(img,img.layers[0],new_filename, new_filename)
	img = pdb.gimp_file_load(filename, filename)
	img.scale(10,7)
	new_filename = '/'.join(filename.split('/')[0:-1]) + "/small/" + filename.split('/')[-1]
	pdb.gimp_file_save(img,img.layers[0],new_filename, new_filename)

o = []
for i in gimp.image_list():
	o.append(i)

for i in o:
	save_mod(i.filename)
	#pdb.gimp_file_save(i,i.layers[0], i.filename, i.filename)