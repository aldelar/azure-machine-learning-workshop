# imports
import argparse, os
# azureml imports
import azureml.core
import azureml.dataprep as dprep

# Script Parameters
parser = argparse.ArgumentParser("args")
parser.add_argument("--h_ts_1", type=str, help="h_ts_1")
parser.add_argument("--h_ts_2", type=str, help="h_ts_2")
parser.add_argument("--h_ts_3", type=str, help="h_ts_3")
parser.add_argument("--d_ts_1", type=str, help="d_ts_1")
parser.add_argument("--d_ts_2", type=str, help="d_ts_2")
parser.add_argument("--output", type=str, help="output")
args = parser.parse_args()

# parse inputs
h_ts_1_dr = args.h_ts_1
h_ts_2_dr = args.h_ts_2
h_ts_3_dr = args.h_ts_3
d_ts_1_dr = args.d_ts_1
d_ts_2_dr = args.d_ts_2

# =======================
# azureml-dataprep-sdk.py
# =======================

h_ts_1_dflow = dprep.auto_read_file(h_ts_1_dr)
h_ts_2_dflow = dprep.auto_read_file(h_ts_2_dr)
h_ts_3_dflow = dprep.auto_read_file(h_ts_3_dr)
d_ts_1_dflow = dprep.auto_read_file(d_ts_1_dr)
d_ts_2_dflow = dprep.auto_read_file(d_ts_2_dr)

# Pivot data
h_ts_1_pivot_dflow = h_ts_1_dflow.pivot(['NODE_ID'],'MW',
                                        azureml.dataprep.api.engineapi.typedefinitions.SummaryFunction.MAX,
                                        ['MYDATE','HOUR'])
h_ts_2_pivot_dflow = h_ts_2_dflow.pivot(['NODE_ID'],'MW',
                                        azureml.dataprep.api.engineapi.typedefinitions.SummaryFunction.MAX,
                                        ['MYDATE','HOUR'])

# merge DATE and HOUR and update datatype for DATETIME column
def ts_merge_date_hour_to_datetime(dflow, date_column_name, hour_column_name):
    # merge columns
    dflow = dflow.derive_column_by_example(
        source_columns = [date_column_name,hour_column_name],
        new_column_name = 'DATETIME',
        example_data = [({date_column_name: '1/1/2012', hour_column_name: '1'},    '01/01/2012 01:00'),
                        ({date_column_name: '10/10/2012', hour_column_name: '15'}, '10/10/2012 15:00'),
                        ({date_column_name: '1/17/2012', hour_column_name: '12'},  '01/17/2012 12:00')]
        ).drop_columns([hour_column_name])
    # update data type
    builder = dflow.builders.set_column_types()
    builder.learn()
    builder.conversion_candidates[date_column_name] = (dprep.FieldType.DATE, ['%m/%d/%Y'])
    builder.conversion_candidates['DATETIME'] = (dprep.FieldType.DATE, ['%m/%d/%Y %H:%M'])
    return builder.to_dataflow()

# generate all DATETIME columns with proper data type
h_ts_1_pivot_dt_dflow = ts_merge_date_hour_to_datetime(h_ts_1_pivot_dflow,'MYDATE','HOUR')
h_ts_2_pivot_dt_dflow = ts_merge_date_hour_to_datetime(h_ts_2_pivot_dflow,'MYDATE','HOUR')
h_ts_3_dt_dflow =       ts_merge_date_hour_to_datetime(h_ts_3_dflow,      'DATE','HE')

# JOINING DATA SET h_ts_dflow=join(h1,h2,h3)
h_ts_dflow = dprep.Dataflow.join(
    dprep.Dataflow.join(h_ts_1_pivot_dt_dflow,
                        h_ts_2_pivot_dt_dflow,
                        join_key_pairs=[('DATETIME', 'DATETIME')],
                        left_column_prefix='h1_',right_column_prefix='h2_'
                       ).drop_columns(['h2_MYDATE','h2_DATETIME']).rename_columns({'h1_MYDATE':'MYDATE','h1_DATETIME':'DATETIME'}),
    h_ts_3_dt_dflow,
    join_key_pairs=[('DATETIME', 'DATETIME')],
    left_column_prefix='',
    right_column_prefix='h3_'
).drop_columns(['h3_DATE','h3_DATETIME'])

# JOINING DATA SET d_ts_dflow=join(d1,d2)
d_ts_dflow = dprep.Dataflow.join(
    d_ts_1_dflow,
    d_ts_2_dflow,
    join_key_pairs=[('RDATE', 'RDATE')],
    left_column_prefix='',
    right_column_prefix='r_').drop_columns(['r_RDATE']).rename_columns({'r_X2':'X2'})

# helper: generate summary column
def generate_summary_column(column_name,column_suffix,summary_function):
    return dprep.SummaryColumnsValue(
                column_id=column_name,
                summary_column_name=column_name+'_'+column_suffix,
                summary_function=summary_function)

# helper: generate summary column for a few functions for each column that's not DATETIME
def generate_summary_columns(dflow):
    summary_columns = []
    for key in h_ts_dflow.get_profile().columns.keys():
        if key != 'MYDATE' and key != 'DATETIME':
            summary_columns.append(generate_summary_column(key,'MAX',dprep.SummaryFunction.MAX))
            summary_columns.append(generate_summary_column(key,'MIN',dprep.SummaryFunction.MIN))
            summary_columns.append(generate_summary_column(key,'MEAN',dprep.SummaryFunction.MEAN))
            summary_columns.append(generate_summary_column(key,'MEDIAN',dprep.SummaryFunction.MEDIAN))
    return summary_columns

# summarize h_ts_dflow to daily
h_ts_summarized_dflow = h_ts_dflow.summarize(
    summary_columns=generate_summary_columns(h_ts_dflow),
    group_by_columns=['MYDATE'])

# join h and d series
training_dflow = dprep.Dataflow.join(
    h_ts_summarized_dflow,
    d_ts_dflow,
    join_key_pairs=[('MYDATE', 'RDATE')],
    left_column_prefix='',
    right_column_prefix='r_').drop_columns(['r_RDATE']).rename_columns({'r_X1':'X1','r_X2':'X2'})

# ===========================
# EOF azureml-dataprep-sdk.py
# ===========================

# writing output
training_dflow.write_to_csv(directory_path=args.output).run_local()