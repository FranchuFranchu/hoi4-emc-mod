import argparse
import csv

csv.register_dialect('hoi4', delimiter=';')
    
has = set([i for i in range(256)])

with open("../map/definition.csv") as f:
    a = csv.reader(f, 'hoi4')
    for row in a:
        last_n = int(row[0])


parser = argparse.ArgumentParser()
parser.add_argument("red_start", type=int)
parser.add_argument("red_end", type=int)
parser.add_argument("green_start", type=int)
parser.add_argument("green_end", type=int)
parser.add_argument("blue_start", type=int)
parser.add_argument("blue_end", type=int)
arg = parser.parse_args()

print("Started adding {}".format(last_n))

with open("../map/definition.csv", "a") as f:

    for r in range(arg.red_start, arg.red_end + 1):
        for g in range(arg.green_start, arg.green_end + 1):
            for b in range(arg.blue_start, arg.blue_end + 1):
                last_n += 1
                f.write("\n{last_n};{r};{g};{b};land;false;plains;3".format(**locals()))

print("End N {}".format(last_n))