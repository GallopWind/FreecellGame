#!python

import pandas as pd
import sys
import DEFINITION
import numpy as np

if __name__ == '__main__':
    data_path = sys.argv[1]
    output_pata = sys.argv[2]
    data = pd.read_csv(data_path, index_col=0, dtype=DEFINITION.DTYPES)
    data.iloc[:, 0:104:2] = data.iloc[:, 0:104:2].astype('float16') / 16.0
    data.iloc[:, 1:104:2] = data.iloc[:, 1:104:2].astype('float16') / 20.0
    data.iloc[:, 104] = data.iloc[:, 104].astype('float16') / 100.0
    data.to_csv(output_pata)
