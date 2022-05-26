# data_organization
Script to organize unaligned metabolomics sample files for individual processing


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

