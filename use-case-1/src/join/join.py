#
from azureml.core import Run, Dataset

#
import argparse, os
import pandas as pd

# Script Parameters
parser = argparse.ArgumentParser("join")
parser.add_argument("--input_1", type=str, help="input_1")
parser.add_argument("--input_2", type=str, help="input_2")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()
print("Input 1: %s" % args.input_1)
print("Input 2: %s" % args.input_2)
print("Output : %s" % args.output)

# Retrieve Input Dataset
input_df_1 = pd.read_csv(args.input_1)
input_df_2 = pd.read_csv(args.input_2)

# Join
output_df = pd.merge(input_df_1,input_df_2,on='DATE',how='inner')

# write output dataset
output_df.to_csv(args.output,index=False,encoding='utf-8')
print("%s created" % args.output)