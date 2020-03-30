import argparse
import os

parser = argparse.ArgumentParser("join")
parser.add_argument("--input_data_1", type=str, help="input_data_1")
parser.add_argument("--input_data_2", type=str, help="input_data_2")
parser.add_argument("--output_data", type=str, help="output_data")

args = parser.parse_args()

print("Argument 1: %s" % args.input_data_1)
print("Argument 2: %s" % args.input_data_2)
print("Argument 3: %s" % args.output_data)

if not (args.output_data is None):
    os.makedirs(args.output_data, exist_ok=True)
    print("%s created" % args.output_data)
