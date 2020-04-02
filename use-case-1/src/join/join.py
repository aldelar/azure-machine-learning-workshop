#
# join: joins 2 or 3 datasets on the same join_column (set input_3 to '' if only 2 datasets to join)
#

#
import argparse, os
import pandas as pd

# Script Parameters
parser = argparse.ArgumentParser("join")
parser.add_argument("--join_column", type=str, help="join_column")
parser.add_argument("--input_1", type=str, help="input_1")
parser.add_argument("--input_2", type=str, help="input_2")
parser.add_argument("--input_3", type=str, help="input_3")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()
print("Join Column: %s" % args.join_column)
print("Input 1: %s" % args.input_1)
print("Input 2: %s" % args.input_2)
print("Input 3: %s" % args.input_3)
print("Output : %s" % args.output)

# Retrieve Input Datasets
# Get data from inputs, which are pre-mounted file paths
input_df_1 = pd.read_csv(args.input_1)
input_df_2 = pd.read_csv(args.input_2)
if args.input_3:
    input_df_3 = pd.read_csv(args.input_3)

# Join Datasets
output_df = input_df_1.merge(input_df_2,on=args.join_column,how='inner',suffixes=('_L1', '_R1'))
if args.input_3:
    output_df = output_df.merge(input_df_3,on=args.join_column,how='inner',suffixes=('_L2', '_R2'))

# write output dataset
output_df.to_csv(args.output,index=False,encoding='utf-8')
print("%s created" % args.output)