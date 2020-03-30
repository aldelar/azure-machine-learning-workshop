import argparse
import os

parser = argparse.ArgumentParser("extract")
parser.add_argument("--input_data", type=str, help="input_data")
parser.add_argument("--output_data", type=str, help="output_data")

args = parser.parse_args()

print("Argument 1: %s" % args.input_data)
print("Argument 2: %s" % args.output_data)

if not (args.output_data is None):
    os.makedirs(args.output_data, exist_ok=True)
    print("%s created" % args.output_data)