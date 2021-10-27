import pandas
import pandas as pd
import numpy as np


def get_lowest_cost(dataframe):
    cost = dataframe.loc[:, 'cost']
    index = cost.argmin(axis=0)
    return dataframe.iloc[index, :]


if __name__ == '__main__':
    data1 = pd.DataFrame(columns=['id', 'cost'], dtype='int')
    data2 = pd.DataFrame(columns=['id', 'cost'], dtype='int')
    data1.loc['hash1'] = [1, 10]
    data1.loc['hash2'] = [2, 12]
    data1.loc['hash3'] = [3, 9]
    data2.loc['hash1'] = [1, 7]
    data2.loc['hash2'] = [2, 14]
    data2.loc['hash3'] = [3, 9]
    data1.to_csv('data/data1.csv')
    data2.to_csv('data/data2.csv')

    data0 = pd.concat([data1, data2])
    group_data = data0.groupby(data0.index)

    merge_data = group_data.apply(get_lowest_cost)
    group_data
