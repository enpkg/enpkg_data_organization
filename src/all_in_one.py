# Loading required libs

import pandas as pd
import numpy as np
import os
import pathlib
import argparse
import textwrap
import shutil 

""" Argument parser """
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
         Organize folder with unaligned feature list files [features spectra file, feature area file and sirius spectra file (optional)] and their aggregated metadata in individual folders
         --------------------------------
            You should just enter the path to the directory where files are located, the aggregated metadata filename and the analysis polarity. 
        '''))
parser.add_argument('--sample_dir_path', required=True,
                    help='The path to the directory where files are located')
parser.add_argument('--metadata_filename', required=True,
                    help='The name of the metadata file to use (it has to be located in sample_dir_path)')
parser.add_argument('--polarity', required=True,
                    help='The polarity mode of LC-MS/MS analyses')
args = parser.parse_args()
sample_dir_path = os.path.normpath(args.sample_dir_path)
metadata_filename = args.metadata_filename
polarity = args.polarity

# test
sample_dir_path = "C:/Users/gaudrya.FARMA/Desktop/test_export_mzmine"
metadata_filename = "metadata.tsv"
polarity = 'pos'

# Loading the df
os.chdir(sample_dir_path)
df_metadata = pd.read_csv(metadata_filename, sep='\t')

# List folder content
content_list = os.listdir(sample_dir_path)

# Function

def organize_folder(df_metadata):
    for i,row in df_metadata.iterrows():
        sample_id = row['sample_id']
        sample_filename = row['sample_filename']
        sample_filename_woext = sample_filename.rsplit('.', 1)[0]
        # create sample's folder
        if not os.path.isdir(sample_id):
            os.makedirs(sample_id)
        
        # create individual metadata file 
        pd.DataFrame(df_metadata.iloc[i], ).transpose().to_csv(sample_id + '/' + sample_id + '_metadata.tsv', sep='\t', index=False)
        
        # move and rename sample's files
        subFolder = os.path.join(os.getcwd(), sample_id + '/')
        for file in content_list:
            if file.startswith(sample_filename_woext):
                shutil.move(os.path.join(os.getcwd(), file), subFolder)
        for file in os.listdir(subFolder):
            if file.endswith('.csv'):
                os.rename(subFolder + file, subFolder + f'{sample_id}_features_quant_{polarity}.csv')
            elif file.endswith('_sirius.mgf'):
                os.rename(subFolder + file, subFolder + f'{sample_id}_sirius_{polarity}.mgf')
            elif file.endswith('.mgf'):
                os.rename(subFolder + file, subFolder + f'{sample_id}_features_ms2_{polarity}.csv')
            
organize_folder(df_metadata)
