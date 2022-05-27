
# Loading required libs

import pandas as pd
import numpy as np
import math
import os
import sys
import pathlib
from pathlib import Path


p = Path(__file__).parents[1]
print(p)
os.chdir(p)


# The aim of this script is to create an individual metadata table form a main metadata table


# defining the paths

working_folder_path = '/Volumes/mapp_metabolomics/DBGI'
individual_files_folder_path = '/Volumes/mapp_metabolomics/DBGI/ind_files'

input_filename = 'manual_dbgi_pilot_metadata'
filename_suffix = 'csv'
path_to_input_file = os.path.join(
    working_folder_path, input_filename + "." + filename_suffix)


# Loading the df

df = pd.read_csv(path_to_input_file,
                 sep=',', encoding='unicode_escape')

# First we create a column which will reflect the folders name established previously

df['clean_filename'] = df['filename'].map(
    lambda x: x.lstrip('20220513_PMA_').rstrip('.mzML'))


df.columns

df.info()


# A path is created by specifying the rootdir and iterating over the metadata clean_filename column

rootdir = pathlib.Path(individual_files_folder_path)


individual_folders_path = df.apply(lambda x: rootdir /
                                   str(x['clean_filename']), axis='columns')


individual_folders_path.drop_duplicates(keep='first', inplace=True)


#the metadata table is filtered to keep only relevant values (these will need to be defined)

df.columns

# here we add a sample type column
df['sample_type'] = np.where(
    df['filename'].str.contains('Ctrl'), 'blank', 'sample')

# specific columns are kept
cols_to_keep = ['filename', 'ATTRIBUTE_query_otol_species',
                'clean_filename', 'sample_type']

df = df[cols_to_keep]

# optionally renamed
df.rename(columns={'clean_filename': 'sample_id',
          'ATTRIBUTE_query_otol_species': 'biological_source'}, inplace=True)

# and re-ordered

df = df[['sample_id', 'biological_source', 'sample_type', 'filename']]

# the following for loop will finally create a tsv file with the individual metadata information per folder

for csvfile, data in df.groupby(individual_folders_path):
    try:
        # print(csvfile, data)
        # csvfile.parent.mkdir(parents=True, exist_ok=True)
        filename = data['sample_id'].values[0] + '_metadata.tsv'
        file = pathlib.Path(csvfile, filename)
        data.to_csv(file, sep='\t', index=False)
    except OSError:
        continue
