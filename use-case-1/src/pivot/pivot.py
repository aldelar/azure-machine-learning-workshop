#
# pivot: normalizes DATE + HOUR columns as DATETIME COLUMN
#        and optionally pivots data if pivot_columns are provided
#

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
parser.add_argument("--date_column", type=str, help="date_column")
parser.add_argument("--hour_column", type=str, help="hour_column")
parser.add_argument("--datetime_column_name", type=str, help="datetime_column_name")
parser.add_argument("--pivot_columns", type=str, help="pivot_columns")
parser.add_argument("--value_column", type=str, help="value_column")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()
print("Date Column: %s" % args.date_column)
print("Hour Column: %s" % args.hour_column)
print("Datetime Column Name: %s" % args.datetime_column_name)
print("Pivot Columns: %s" % args.pivot_columns)
print("Value Column: %s" % args.value_column)
print("Output: %s" % args.output)

# Retrieve Input Dataset
input_ds = Run.get_context().input_datasets["time_series"]

# Read dataset as a DataFrame
input_df = input_ds.to_pandas_dataframe()
# NOTE: Ability to develop/work on samples from the original dataset (0.01 = 1% of full dataset)
# input_df = input_dataset.take_sample(0.01).to_pandas_dataframe()

# Generate timestamp column 'DATETIME' FROM date AND hour columns
input_df[args.datetime_column_name] = input_df.apply(lambda x: gen_date(x[args.date_column], x[args.hour_column]), axis=1)
# Drop date AND hour columns
input_df = input_df.drop(columns=[args.date_column,args.hour_column])
# Pivot Data
if args.pivot_columns:
    # pivot and set index to datetime
    output_df = pd.pivot_table(input_df, values=args.value_column, index=args.datetime_column_name, columns=args.pivot_columns, aggfunc=np.max)
else:
    # set index to datetime
    output_df = input_df.set_index(args.datetime_column_name)

# write output dataset
output_df.to_csv(args.output,encoding='utf-8')
print("%s created" % args.output)