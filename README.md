# data_organization
Script to organize unaligned metabolomics sample files for individual processing

## Workflow

For each ionization mode, proceed as follows:

### 1) MzMine2 processing

In MzMine 2, process your files according to the [FBMN workflow](https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking-with-mzmine2/) until the "Isotope Grouping" step. At this step, filter the obtained feature lists to keep only features linked to an MS/MS spectrum.

Once this is done, export all your **unaligned** feature lists using the "Export to GNPS" module. Select the targeted folder and as a filename insert empty curly brackets so MzMine will name files according to the feature list names (ex: "path/to/your/data/directory/{}"). Do the same using the "Export to Sirius" module, this time adding a "_sirius" suffix (ex: "path/to/your/data/directory/{}_sirius.mgf"). 
**Export pos and neg data in 2 separate folders.**

### 2) .tsv metadata file formatting

**5 columns are required**: sample_filename_pos, sample_filename_neg, sample_id, sample_type & sample_organism.
NB: if you have only pos files, no need for sample_filename_neg column (and the opposite if you have only neg files).

- **sample_filename_pos**: the name of the mzML or mzXML LC-MS file (ex: 211027_AG_ZC012714_pos_20211028181555.mzML)
- **sample_filename_neg**: the name of the mzML or mzXML LC-MS file (ex: 211027_AG_ZC012714_neg_20211029132336.mzML)
- **sample_id**: the sample ID correspinding to the file (ex: AG_ZC012714)
- **sample_type**: one of QC, blank or sample (ex: sample)
- **organism_species**: for samples (not QC and blanks), species name of the sample in binomial nomenclature (ex: Ailanthus altissima)

You can of course add as many additional columns as you wish (bioactivity, injection date, LC method, ...).
An example of metadata file can be found [here](https://github.com/mandelbrot-project/data_organization/blob/main/data/metadata.tsv).

Finally, place the .tsv metadata file in the folder where you exported your feature lists files. 

### 3) Create architecture!

Once this is done, lauch the create_architecture.py script to organize your files using the following command adapted to your case:

```console
python .\src\create_architecture.py --source_path path/to/your/data/directory/ --target_path path/to/your/data/ouptut/  --metadata_filename metadatafilename.tsv --polarity pos
```
If existing, do the same for the other ionization mode (using the same target_path).

```console
python .\src\create_architecture.py --source_path path/to/your/data/directory/ --target_path path/to/your/data/ouptut/  --metadata_filename metadatafilename.tsv --polarity neg
```
For help with the arguments:

```console
python .\src\create_architecture.py --help
```

## Desired architecture

```
data/
└─── sample_a/
|     |  sample_a_metadata.tsv
|     └─── pos/
|     |     sample_a_features_quant_pos.csv
|     |     sample_a_features_ms2_pos.mgf
|     |     sample_a_sirius_pos.mgf
|     └─── neg/
|           sample_a_features_quant_neg.csv
|           sample_a_features_ms2_neg.mgf
|           sample_a_sirius_neg.mgf
|
└─── sample_b/
|
└─── sample_n/
```
NB: In this example both pos and neg ionization mode are present for samples, but to have only one is fine too.

