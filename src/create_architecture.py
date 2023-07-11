import pandas as pd
import os
import argparse
import textwrap
import shutil

""" Argument parser """
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        Organize folder with unaligned feature list files [features spectra file, feature area file \
            and sirius spectra file (optional)] and their aggregated metadata in individual folders
         --------------------------------
        You should just enter the path to the directory where files are located, \
            the aggregated metadata filename and the analysis polarity. 
        '''))

parser.add_argument('--source_path', required=True,
                    help='The path to the directory where data files are located')
parser.add_argument('--source_metadata_path', required=True,
                    help='The path to the directory where metadata files are located')
parser.add_argument('--target_path', required=True,
                    help='The path to the directory where files will be moved')
parser.add_argument('--sample_metadata_filename', required=True,
                    help='The name of the metadata file to use (it has to be located in sample_dir_path)')
parser.add_argument('--lcms_method_params_filename', required=True,
                    help='The name of the metadata file to use (it has to be located in sample_dir_path)')
parser.add_argument('--lcms_processing_params_filename', required=True,
                    help='The name of the metadata file to use (it has to be located in sample_dir_path)')
parser.add_argument('--polarity', required=True,
                    help='The polarity mode of LC-MS/MS analyses')

args = parser.parse_args()
source_path = os.path.normpath(args.source_path)
source_metadata_path = os.path.normpath(args.source_metadata_path)
target_path = os.path.normpath(args.target_path)
metadata_filename = args.sample_metadata_filename
lcms_method_filename = args.lcms_method_params_filename
lcms_processing_filename = args.lcms_processing_params_filename
polarity = args.polarity


# Create target path if does not exist
if not os.path.isdir(target_path):
    os.makedirs(target_path)

# Loading the metadata
path_metadata = os.path.join(source_metadata_path, metadata_filename)
df_metadata = pd.read_csv(path_metadata, sep='\t')

path_lcms_method_filename = os.path.join(source_metadata_path, lcms_method_filename)
path_lcms_processing_filename = os.path.join(source_metadata_path, lcms_processing_filename)

# List folder content
content_list = os.listdir(source_path)

# Function
def organize_folder(df_metadata, path_lcms_method_filename, path_lcms_processing_filename):
    if not os.path.isdir(os.path.join(target_path, f'for_massive_upload_{polarity}')):
        os.makedirs(os.path.join(target_path, f'for_massive_upload_{polarity}'))
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
        sample_folder = os.path.join(target_path, sample_id)
        if not os.path.isdir(sample_folder):
            os.makedirs(sample_folder)
        
        # create individual metadata file 
        pd.DataFrame(df_metadata.iloc[i], ).transpose().to_csv(os.path.join(target_path, sample_id, sample_id + '_metadata.tsv'), sep='\t', index=False)

        # move and rename sample's files
        sub_folder = os.path.normpath(os.path.join(sample_folder, polarity + '/'))
        if not os.path.isdir(sub_folder):
            os.makedirs(sub_folder)

        for file in content_list:
            if file.startswith(sample_filename_woext):
                shutil.copy(os.path.join(source_path, file), sub_folder)

        if len(os.listdir(sub_folder)) == 0:
            print(f'No matched file for sample {sample_id}')
        elif len(os.listdir(sub_folder)) == 1:
            print(f'1 matched file for sample {sample_id}')
        elif len(os.listdir(sub_folder)) == 2:
            print(f'2 matched file for sample {sample_id}')
        elif len(os.listdir(sub_folder)) == 3:
            print(f'3 matched file for sample {sample_id}')

        for file in os.listdir(sub_folder):
            file_path = os.path.normpath(os.path.join(sub_folder + '/' + file))

            lcms_method_extension = path_lcms_method_filename.split(".",1)[1]
            lcms_processing_extension = path_lcms_processing_filename.split(".",1)[1]
            destination_path_lcms_method_filename = os.path.join(sub_folder, f'{sample_id}_lcms_method_params_{polarity}.{lcms_method_extension}')
            destination_path_lcms_processing_filename = os.path.join(sub_folder, f'{sample_id}_lcms_processing_params_{polarity}.{lcms_processing_extension}')
            shutil.copyfile(path_lcms_method_filename, destination_path_lcms_method_filename)
            shutil.copyfile(path_lcms_processing_filename, destination_path_lcms_processing_filename)

            if file.endswith('.csv'):
                os.rename(file_path, os.path.join(sub_folder, f'{sample_id}_features_quant_{polarity}.csv'))
            elif file.endswith('_sirius.mgf'):
                os.rename(file_path, os.path.join(sub_folder, f'{sample_id}_sirius_{polarity}.mgf'))
            elif file.endswith('.mgf'):
                os.rename(file_path, os.path.join(sub_folder, f'{sample_id}_features_ms2_{polarity}.mgf'))
                shutil.copy((sub_folder + '/' + f'{sample_id}_features_ms2_{polarity}.mgf'), os.path.join('..', target_path, f'for_massive_upload_{polarity}'))

organize_folder(df_metadata=df_metadata, path_lcms_method_filename=path_lcms_method_filename,
                path_lcms_processing_filename=path_lcms_processing_filename)
