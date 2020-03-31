#
from azureml.core import Workspace, Dataset, Run
from azureml import DataTypeIds

#
import argparse, os
import datetime as dt
import pandas as pd
import numpy as np

# generates date from DATE + HOUR
def gen_date(d,h):
    return d + dt.timedelta(hours=int(h))

# Pivot Parameters
parser = argparse.ArgumentParser("extract")
parser.add_argument("--input_dataset", type=str, help="input_dataset")
parser.add_argument("--output_dataset", type=str, help="output_dataset")
args = parser.parse_args()
print("Input DataSet: %s" % args.input_dataset)
print("Output DataSet: %s" % args.output_dataset)

# Retrieve Input Dataset
ws = Workspace.from_config()
input_dataset = Dataset.get_by_name(ws, name=args.input_dataset)

# ability to develop/work on samples from the original dataset (0.01 = 1% of full dataset)
#input_df = input_dataset.take_sample(0.01).to_pandas_dataframe()
input_df = input_dataset.to_pandas_dataframe()
print(input_df)

# Generate timestamp column 'DATE' FROM 'MYDATE' and 'HOUR'
input_df['DATE'] = input_df.apply(lambda x: gen_date(x.MYDATE, x.HOUR), axis=1)
input_df = input_df[['DATE','NODE_ID','MW']]

# Pivot Data
output_df = pd.pivot_table(input_df, values='MW', index='DATE', columns='NODE_ID', aggfunc=np.max)

# write output dataset
dataset = ws.datasets.add_from_dataframe(
    dataframe=output_df,
    data_type_id=DataTypeIds.GenericCSV,
    name=args.output_dataset
)