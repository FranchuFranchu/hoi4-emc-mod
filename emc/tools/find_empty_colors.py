import csv

csv.register_dialect('hoi4', delimiter=';')
    
has = set([i for i in range(256)])

with open("../map/definition.csv") as f:
    a = csv.reader(f, 'hoi4')
    for row in a:
        row[1] = int(row[1])
        if row[1] in has:
            has = has - set([row[1]])
            if len(has) == 0:
                break

print(has)
# List of Red values with no colors assigned to them
# {139, 140, 141, 145, 146, 147, 149, 152, 154, 157, 159, 160, 161, 163, 166, 180, 182, 185, 187, 189, 192, 194, 197, 200, 201, 202, 203, 204, 207, 209, 216, 217, 218, 221, 222, 227, 231, 234, 235, 237, 239, 240, 241, 242, 243, 244, 248, 249, 250, 252}



