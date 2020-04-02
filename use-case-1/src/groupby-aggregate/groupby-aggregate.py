#
# grouby-aggregate: groups by date and generate aggregates for each value column
#

#
#from azureml.core import Run, Dataset
#
import argparse, os
import pandas as pd
import numpy as np
import dateutil

# Script Parameters
parser = argparse.ArgumentParser("groupby-aggregate")
parser.add_argument("--datetime_column", type=str, help="datetime_column")
parser.add_argument("--date_column_name", type=str, help="date_column_name")
parser.add_argument("--input_ds", type=str, help="input_ds")
parser.add_argument("--output_ds", type=str, help="output_ds")
args = parser.parse_args()
print("Datetime Column: %s" % args.datetime_column)
print("Date Column Name: %s" % args.date_column_name)
print("Input : %s" % args.input_ds)
print("Output : %s" % args.output_ds)

# Retrieve Input Datasets
# Get data from inputs, which are pre-mounted file paths
#input_ds = Run.get_context().input_datasets["input"]
#input_df = input_ds.to_pandas_dataframe()

input_df = pd.read_csv(args.input_ds)

# Generate DATE column
input_df[args.date_column_name] = input_df.apply(lambda x: dateutil.parser.parse(x[args.datetime_column]).date(), axis=1)

# Aggregates
output_df = input_df.groupby(args.date_column_name).aggregate([min, max, sum, np.median, np.mean, np.std])
output_df.columns = output_df.columns.to_series().str.join('_')

# write output dataset
output_df.to_csv(args.output_ds,index=False,encoding='utf-8')
print("%s created" % args.output)