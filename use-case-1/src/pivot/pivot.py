#
from azureml.core import Run, Dataset

#
import argparse, os
import datetime as dt
import pandas as pd
import numpy as np

# generates date from DATE + HOUR
def gen_date(d,h):
    return d + dt.timedelta(hours=int(h))

# Script Parameters
parser = argparse.ArgumentParser("pivot")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()
print("Output: %s" % args.output)

# Retrieve Input Dataset
run_context = Run.get_context()
input_ds = run_context.input_datasets["time_series"]

# Read dataset as a DataFrame
input_df = input_ds.to_pandas_dataframe()
# NOTE: Ability to develop/work on samples from the original dataset (0.01 = 1% of full dataset)
# input_df = input_dataset.take_sample(0.01).to_pandas_dataframe()

# Generate timestamp column 'DATE' FROM 'MYDATE' and 'HOUR'
input_df['DATE'] = input_df.apply(lambda x: gen_date(x.MYDATE, x.HOUR), axis=1)
# Only keep necessary columns
input_df = input_df[['DATE','NODE_ID','MW']]
# Pivot Data
output_df = pd.pivot_table(input_df, values='MW', index='DATE', columns='NODE_ID', aggfunc=np.max)

# write output dataset
output_df.to_csv(args.output,encoding='utf-8')
print("%s created" % args.output)