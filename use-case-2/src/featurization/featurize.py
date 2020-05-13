#
# featurize:
#   DATETIME = DATE + HOUR columns
#
from azureml.core import Run, Dataset

# misc imports
import argparse, os
import datetime as dt
import pandas as pd
import numpy as np

# generates date from DATE + HOUR
def gen_date(d,h):
    return d + dt.timedelta(hours=int(h))

# Script Parameters
parser = argparse.ArgumentParser("featurize")
parser.add_argument("--date_column", type=str, help="date_column")
parser.add_argument("--hour_column", type=str, help="hour_column")
parser.add_argument("--datetime_column_name", type=str, help="datetime_column_name")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()
print("Date Column: %s" % args.date_column)
print("Hour Column: %s" % args.hour_column)
print("Datetime Column Name: %s" % args.datetime_column_name)
print("Output Data: %s" % args.output)

# Retrieve Input Dataset
input_ds = Run.get_context().input_datasets["input"]
input_df = input_ds.to_pandas_dataframe()

# Generate timestamp column 'DATETIME' FROM date AND hour columns
input_df[args.datetime_column_name] = input_df.apply(lambda x: gen_date(x[args.date_column], x[args.hour_column]), axis=1)
# Drop date AND hour columns
input_df = input_df.drop(columns=[args.date_column,args.hour_column])

# write output dataset
input_df.to_csv(args.output,encoding='utf-8')
print("%s created" % args.output)