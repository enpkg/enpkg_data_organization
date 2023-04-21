# enpkg_data_organization
Script to organize unaligned metabolomics sample files for individual processing and (optionally) add MassIVE id to metadata.

⚙️ Workflow part of [enpkg_workflow](https://github.com/enpkg/enpkg_workflow).  

## Workflow

For each ionization mode, proceed as follows:

### 1) MzMine2 processing

In MzMine 2, process your files according to the [FBMN workflow](https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking-with-mzmine2/) until the "Isotope Grouping" step. At this step, filter the obtained feature lists to keep only features linked to an MS/MS spectrum.  
:warning: Don't forget to use "Reset feature ID" when filtering features with MS/MS only. This will cause inconsistencies in GNPS links if not done.

Once this is done, export all your **unaligned** feature lists using the "Export to GNPS" module. Select the targeted folder and as a filename insert empty curly brackets so MzMine will name files according to the feature list names (ex: "path/to/your/data/directory/{}"). Do the same using the "Export to Sirius" module, this time adding a "_sirius" suffix (ex: "path/to/your/data/directory/{}_sirius.mgf"). 


**Export pos and neg data in 2 separate folders.**

### 2) .tsv metadata file formatting

**4 columns are required**: sample_filename_pos (and/or sample_filename_neg), sample_id, sample_type & sample_organism.
NB: if you have only pos files, no need for sample_filename_neg column (and the opposite if you have only neg files).

- **sample_filename_pos**: the name of the mzML or mzXML LC-MS file (ex: 211027_AG_ZC012714_pos_20211028181555.mzML)
- **sample_filename_neg**: the name of the mzML or mzXML LC-MS file (ex: 211027_AG_ZC012714_neg_20211029132336.mzML)
- **sample_id**: the sample ID corresponding to the file (ex: AG_ZC012714)
- **sample_type**: one of QC, blank or sample (ex: sample)
- **sample_substance_name**: the ID of the biological material used to prepare the sample. For example, the ID of the raw plant material used to generate the extract.
- **organism_species**: for samples (not QC and blanks), species name of the sample_substance_name in binomial nomenclature (ex: Ailanthus altissima)

You can of course add as many additional columns as you wish (bioactivity, injection date, LC method, ...).
An example of metadata file can be found [here](https://github.com/enpkg/enpkg_data_organization/blob/main/data/metadata.tsv).

Finally, place the .tsv metadata file in the folder where you exported your feature lists files. 

### 3) Create architecture!

Once this is done, lauch the create_architecture.py script to organize your files using the following command adapted to your case:
Note: on Unix system make sure to change \ to / 

```console
python .\src\create_architecture.py --source_path path/to/your/data/in/directory/ --target_path path/to/your/data/out/directory/  --metadata_filename metadatafilename.tsv --polarity pos
```
If existing, do the same for the other ionization mode (using the same target_path).

```console
python .\src\create_architecture.py --source_path path/to/your/data/in/directory/ --target_path path/to/your/data/out/directory/  --metadata_filename metadatafilename.tsv --polarity neg
```
For help with the arguments:

```console
python .\src\create_architecture.py --help
```

## Desired architecture

```
data/
└─── sample_a/
|     └─── sample_a_metadata.tsv                     # Metadata of sample_a
|     └─── pos/
|     |     sample_a_features_quant_pos.csv          # Features intensity table in positive mode
|     |     sample_a_features_ms2_pos.mgf            # Features fragmentations spectra in positive mode
|     |     sample_a_sirius_pos.mgf                  # Features fragmentations spectra for sirius (with MS1 isotope pattern) in positive mode 
|     └─── neg/
|           sample_a_features_quant_neg.csv
|           sample_a_features_ms2_neg.mgf
|           sample_a_sirius_neg.mgf
|
└─── sample_b/
|
└─── sample_n/
|
└─── for_massive_upload_pos/                         # All *_features_ms2_pos.mgf files ready for upload on MassIVE
|     └─── sample_a_features_ms2_pos.mgf                     
|     └─── ...                    
|     └─── sample_n_features_ms2_pos.mgf
|
└─── for_massive_upload_neg/                         # All *_features_ms2_neg.mgf files ready for upload on MassIVE
      └─── sample_a_features_ms2_neg.mgf                    
      └─── ...                    
      └─── sample_n_features_ms2_neg.mgf                    
```

NB: In this example both pos and neg ionization mode are present for samples, but having only one is fine too.

### 4) Add GNPS MassIVE information

To enjoy links to [GNPS LCMS dasboard](https://gnps-lcms.ucsd.edu/) and visualization of your MS/MS spectra directly from the knowldege graph, we recommend you to upload you data (.mz(X)ML files and feature_MS2_pos/neg.mgf) to the [GNPS MassIVE](https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp) repository. For an easy upload of your features' fragmentation spectra, you can directly upload the content of the **for_massive_upload_<ionization_mode>** folder(s). See GNPS documentation for details on the MassIVE upload process https://ccms-ucsd.github.io/GNPSDocumentation/datasets/ 

:warning: The filenames of the .mz(X)ML files you upload on MassIVE have to match the filenames in your metadata file.

Once this is done, add the MassIVE ID to the medatadata using the following command:

```console
python .\src\add_massive_id.py --massive_id {massive_id} -p {path/to/your/data/ouptut/}
```

### 5) Next step ...

https://github.com/enpkg/enpkg_taxo_enhancer


