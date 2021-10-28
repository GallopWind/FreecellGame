import pandas
import sys

import pandas as pd

NAMES = ['primary_key']
for x in range(52):
    NAMES.append(('%02d' % x) + 'id')
    NAMES.append(('%02d' % x) + 'index')
NAMES.append('cost')

DTYPES = dict()
DTYPES[NAMES[0]] = 'str'
for x in range(1, 106):
    DTYPES[NAMES[x]] = 'uint8'


def select_lowest_cost(dataframe):
    cost = dataframe.loc[:, 'cost']
    index = cost.argmin(axis=0)
    return dataframe.iloc[index, :]


if __name__ == '__main__':
    '''
        Usage: cmd data1 data2 data_out
    '''
    data_bags_name = sys.argv[1:-1]
    output_data_bag_name = sys.argv[-1]
    data_frames = []
    for bag_name in data_bags_name:
        data = pd.read_csv('data/' + bag_name, index_col=0, dtype=DTYPES)
        data_frames.append(data)
    concat_data = pd.concat(data_frames, axis=0)
    merge_data = concat_data.groupby(concat_data.index).apply(select_lowest_cost)
    merge_data.to_csv('data/' + output_data_bag_name)
