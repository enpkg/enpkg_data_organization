# Loading required libs

import pandas as pd
import numpy as np
import os
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

parser.add_argument('--source_path', required=True,
                    help='The path to the directory where data files are located')
parser.add_argument('--target_path', required=True,
                    help='The path to the directory where files will be moved')
parser.add_argument('--metadata_filename', required=True,
                    help='The name of the metadata file to use (it has to be located in sample_dir_path)')
parser.add_argument('--polarity', required=True,
                    help='The polarity mode of LC-MS/MS analyses')

args = parser.parse_args()
source_path = os.path.normpath(args.source_path)
target_path = os.path.normpath(args.target_path)
metadata_filename = args.metadata_filename
polarity = args.polarity

# source_path = os.path.normpath("C:/Users/gaudrya.FARMA/Desktop/bckp/")
# target_path = os.path.normpath("C:/Users/gaudrya.FARMA/Desktop/test_may22/")
# metadata_filename = 'metadata.tsv'
# polarity = 'pos'

# Create target path if does not exist
if not os.path.isdir(target_path):
    os.makedirs(target_path)

# Loading the df
path_metadata = os.path.join(source_path, metadata_filename)
df_metadata = pd.read_csv(path_metadata, sep='\t')

# List folder content
content_list = os.listdir(source_path)

# Function

def organize_folder(df_metadata):
    for i,row in df_metadata.iterrows():
        sample_id = row['sample_id']
        if polarity == 'pos':
            sample_filename = row['sample_filename_pos']
            sample_filename_woext = sample_filename.rsplit('.', 1)[0]
        elif polarity == 'neg':
            sample_filename = row['sample_filename_neg']
            sample_filename_woext = sample_filename.rsplit('.', 1)[0]
        else:
            raise ValueError("Polarity has to be one of [pos, neg]")
        
        # create sample's folder if if it does not exist yet
        sampleFolder = os.path.join(target_path, sample_id)
        if not os.path.isdir(sampleFolder):
            os.makedirs(sampleFolder)
        
        # create individual metadata file 
        pd.DataFrame(df_metadata.iloc[i], ).transpose().to_csv(target_path + '/' + sample_id + '/' + sample_id + '_metadata.tsv', sep='\t', index=False)
        
        # move and rename sample's files
        subFolder = os.path.normpath(os.path.join(sampleFolder + '/' + polarity + '/'))
        if not os.path.isdir(subFolder):
            os.makedirs(subFolder)
        
        for file in content_list:
            if file.startswith(sample_filename_woext):
                shutil.copy(os.path.join(source_path, file), subFolder)
                
        if len(os.listdir(subFolder)) == 0:
            print(f'No matched file for sample {sample_id}')
        elif len(os.listdir(subFolder)) == 1:
            print(f'1 matched file for sample {sample_id}')
        elif len(os.listdir(subFolder)) == 2:
            print(f'2 matched file for sample {sample_id}')
        elif len(os.listdir(subFolder)) == 3:
            print(f'3 matched file for sample {sample_id}')
                
        for file in os.listdir(subFolder):
            file_path = os.path.normpath(os.path.join(subFolder + '/' + file))
            if file.endswith('.csv'):
                os.rename(file_path, os.path.normpath(subFolder + '/' + f'{sample_id}_features_quant_{polarity}.csv'))
            elif file.endswith('_sirius.mgf'):
                os.rename(file_path, os.path.normpath(subFolder + '/' + f'{sample_id}_sirius_{polarity}.mgf'))
            elif file.endswith('.mgf'):
                os.rename(file_path, os.path.normpath(subFolder + '/' + f'{sample_id}_features_ms2_{polarity}.mgf'))
            
organize_folder(df_metadata)
