# data_organization
Script to organize unaligned metabolomics sample files for individual processing

## Desired architecture

```
data
└─── sample_a
|       sample_a_metadata.tsv
|       sample_a_features_quant_pos/neg.csv
|       sample_a_features_ms2_pos/neg.mgf
|       sample_a_sirius_pos/neg.mgf
|
└─── sample_b
|
└─── sample_n
```

## Workflow

### 1) MzMine2 processing

In MzMine 2, process your file according to the [FBMN workflow](https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking-with-mzmine2/) until the "Isotope Grouping" step. At this step, filter the obtained feature lists to keep only features linked to an MS/MS spectrum.

Once this is done, export all your **unaligned** feature lists using the "Export to GNPS" module. Select the targeted folder and as a filename insert empty curly brackets so MzMine will name files according to the feature list names (ex: "path/to/your/data/directory/{}"). Do the same using the "Export to Sirius" module, this time adding a sirius suffix (ex: "path/to/your/data/directory/{}_sirius.mgf").

### 2) .tsv metadata file formatting

4 columns are required: sample_filename, sample_id, sample_type & sample_organism.

- sample_filename: the name of the mzML or mzXML LC-MS file (ex: 211027_AG_ZC012714_pos_20211028181555.mzML)
- sample_id: the sample ID correspinding to the file (ex: AG_ZC012714)
- sample_type: one of QC, blank or sample (ex: sample)
- sample_organism: for samples (not QC and blanks), organism of the sample in binomial nomenclature (ex: Ailanthus altissima)

You can of course add as many additional columns as you wish (bioactivity, injection date, LC method, ...).
An example of metadata file can be found [here](https://github.com/mandelbrot-project/data_organization/blob/main/data/metadata.tsv).

Finally, place the .tsv metadata file in the folder where you exported your feature lists files. 

### 3) Create architecture!

Once this is done, lauch the create_architecture.py script to organize your files:

```console
python .\src\create_architecture.py --sample_dir_path path/to/your/data/directory/ --metadata_filename metadatafilename.tsv --polarity pos
```

For help with the arguments:

```console
python .\src\create_architecture.py --help
```


## Some instruction in bash 
(cleaner scripts later on)

### Remove a given prefix from files

```
for file in 20220513_PMA_*;
do
    mv "$file" "${file##20220513_PMA_}"
done
```

### Rename specific extensions to another pattern

```
for f in *.mgf; do 
    mv -- "$f" "${f%.mgf}_features_ms2_pos.mgf"
done
```

### According to a given pattern create subfolder named with the pattern and mv files to subfolders

```
for i in `ls -ltrh directorypath| awk '{print $NF}'| awk -F "_f|_s" '{print $1}'| sort| uniq`; do mkdir $i; yes|mv  $i* $i; done
```

