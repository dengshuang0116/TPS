#!/usr/bin/env python3

import pandas as pd
import sys
from math import exp as e
import numpy as np
# from tabulate import tabulate  # tabulate with print can work fine when test

def determin_branch(node: pd.core.frame.DataFrame, row: pd.core.frame.DataFrame):
    right_part = node.loc[node['name'] == 'Intercept']['value'] + node[node['name'].str.startswith("hsa")].apply(lambda x: row[x['name']] * x['value'], axis = 1).sum()
    p = e(right_part) / (1 + e(right_part))
    if (p > node.loc[node['name'] == 'P_th']['value']).bool():
        return True
    else:
        return False

def decision(row):
    # We can NOT determin patients without their gender information 
    if row['gender'] == 'Unknown':
        print('Unknown')
        return
    # Check Node 1
    # Should check liver metastasis first in order to take advantage of short circuit
    # Liver metastasis cases were not allowed to be classified as originating from liver tissue
    if row['is_liver_metastasis'] == 0 and determin_branch(model.loc[1], row):
        print('Liver')
    # Female has no testical
    elif row['gender'] == 'Female' and determin_branch(model.loc[2], row):
        print('Testis')
    elif determin_branch(model.loc[3], row):
        if determin_branch(model.loc[12], row):
            if determin_branch(model.loc[13], row):
                if determin_branch(model.loc[14], row):
                    print('Colon')
                elif determin_branch(model.loc[15], row):
                    print('Stomach')
                else:
                    print('Pancreas')
            else:
                print('Lung (carcinoid)')
        elif determin_branch(model.loc[16], row):
            # Use short circuit again
            # Female has no prostate
            if row['gender'] == 'Female' or determin_branch(model.loc[17], row):
                print('Breast')
            else:
                print('Prostate')
        elif determin_branch(model.loc[18], row):
            if determin_branch(model.loc[19], row):
                print('Thyroid')
            # They're male! Male! Male!
            elif row['gender'] == 'Male' or determin_branch(model.loc[20], row):
                if determin_branch(model.loc[21], row):
                    print('Lung')
                else:
                    print('Bladder')
            elif determin_branch(model.loc[22], row):
                print('Endometrium')
            else:
                print('Ovary')
        elif determin_branch(model.loc[23], row):
            print('Thymus (B3)')
        elif determin_branch(model.loc[24], row):
            print('Lung (squamous)')
        else:
            print('Head & neck')
    elif determin_branch(model.loc[4], row):
        if determin_branch(model.loc[5], row):
            print('Lymph node')
        else:
            print('Melanocytes')
    elif determin_branch(model.loc[6], row):
        print('Brain')
    elif determin_branch(model.loc[7], row):
        print('Meninges')
    elif determin_branch(model.loc[8], row):
        print('Thymus (B2)')
    elif determin_branch(model.loc[9], row):
        if determin_branch(model.loc[11], row):
            print('Sarcoma')
        else:
            print('GIST')
    elif determin_branch(model.loc[10], row):
        print('Lung-pleura')
    else:
        print('Kidney')


if __name__ == "__main__":
    # File has lines with only comma, so ignore them as comments
    # The first line will be recognized as header by default
    model = pd.read_csv(sys.argv[1], comment = ',', header = None, names = ['node', 'name', 'value'])
    mi = pd.read_csv(sys.argv[2])
    # To make expression value log-scaled
    mi.loc[:, mi.columns.str.startswith('hsa')] = mi.loc[:, mi.columns.str.startswith('hsa')].apply(np.log)
    # Use node number as index, so model.loc[12] refer to node 12
    model = model.set_index(['node'])
    for _, row in mi.iterrows():
        decision(row)
