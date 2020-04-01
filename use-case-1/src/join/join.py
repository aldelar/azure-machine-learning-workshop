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
run_context = Run.get_context()
input_ds_1 = run_context.input_datasets[args.input_1]
input_ds_2 = run_context.input_datasets[args.input_2]
input_df_1 = input_ds_1.to_pandas_dataframe()
input_df_2 = input_ds_2.to_pandas_dataframe()

# Join
output_df = pd.merge(input_df_1,input_df_2,on='DATE',how='inner')

# write output dataset
output_df.to_csv(args.output,index=False,encoding='utf-8')
print("%s created" % args.output)