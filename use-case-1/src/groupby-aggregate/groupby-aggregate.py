#
# grouby-aggregate: groups by date and generate aggregates for each value column
#

import argparse, os
import pandas as pd
import numpy as np
import dateutil

# Script Parameters
parser = argparse.ArgumentParser("groupby-aggregate")
parser.add_argument("--datetime_column", type=str, help="datetime_column")
parser.add_argument("--date_column_name", type=str, help="date_column_name")
parser.add_argument("--input_pd", type=str, help="input_pd")
parser.add_argument("--output_pd", type=str, help="output_pd")
args = parser.parse_args()
print("Datetime Column: %s" % args.datetime_column)
print("Date Column Name: %s" % args.date_column_name)
print("Input : %s" % args.input_pd)
print("Output : %s" % args.output_pd)

# Retrieve input dataset
input_df = pd.read_csv(args.input_pd)

# Generate DATE column
input_df[args.date_column_name] = input_df.apply(lambda x: dateutil.parser.parse(x[args.datetime_column]).date(), axis=1)

# Aggregates
output_df = input_df.groupby(args.date_column_name).aggregate([min, max, sum, np.median, np.mean, np.std])
output_df.columns = output_df.columns.to_series().str.join('_')
output_df[args.date_column_name] = output_df.index

# write output dataset
output_df.to_csv(args.output_pd,index=False,encoding='utf-8')
print("%s created" % args.output_pd)