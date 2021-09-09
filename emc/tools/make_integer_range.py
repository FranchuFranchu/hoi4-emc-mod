import argparse
import csv


parser = argparse.ArgumentParser()
parser.add_argument("from_", type=int)
parser.add_argument("to", type=int)
arg = parser.parse_args()

print(' '.join([str(i) for i in range(arg.from_, arg.to + 1)]))