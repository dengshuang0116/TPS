# TPS

> The tools implemented/integrated in this project will use pretty complex environment. To satisfy it, I'll deploy a docker image in the future.

## Introduction

Cancer of unknown primary origin(CUP), a metastatic disease with no definite primary site, accounts for nearly 3-5% of new cancer cases[1]. Lots of outstanding researchers have made a big effort in developing tools or methods to solve current limitation in cancer origin identification. Here, we represented TPS: Tumor Positioning Server, an interactive, web-based platform synthesized all published cancer origin prediction methods, to provide a convenient and comprehensive tool for CUP diagnosis community.

## Methods

### Existed tools

| Tool name                                                        | Reference                                                                                                                                                             |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [CancerLocator](https://github.com/jasminezhoulab/CancerLocator) | [CancerLocator: non-invasive cancer diagnosis and tissue-of-origin prediction using methylation profiles of cell-free DNA](https://doi.org/10.1186/s13059-017-1191-5) |
|[MONOD2](https://github.com/dinhdiep/MONOD2) | [Identification of methylation haplotype blocks aids in deconvolution of heterogeneous tissue samples and tumor tissue-of-origin mapping from plasma DNA](http://dx.doi.org/10.1038/ng.3805)
|[TumorTracer](http://www.cbs.dtu.dk/services/TumorTracer)[*] | [TumorTracer: a method to identify the tissue of origin from the somatic mutations of a tumor specimen](https://doi.org/10.1186/s12920-015-0130-0)
|[Methylation Atlas Deconvolution](https://github.com/nloyfer/meth_atlas) | [Comprehensive human cell-type methylation atlas reveals origins of circulating cell-free DNA in health and disease](https://doi.org/10.1038/s41467-018-07466-6)
|[DeepGene](https://github.com/yuanyc06/deepgene) | [DeepGene: an advanced cancer type classifier based on deep learning and somatic point mutations](https://doi.org/10.1186/s12859-016-1334-9)
| [MMCOP](http://server.malab.cn/MMCOP/)[*] | [Tumor origin detection with tissue-specific miRNA and DNA methylation markers](https://doi.org/10.1093/bioinformatics/btx622)

[*]: These tools were implemented as web server.

### Method already provided but implemented by us

#### [Decision-tree classification algorithm using miRNA expression levels](./miRNATreeClassifier), [Ref](http://www.nature.com/doifinder/10.1038/nbt1392)

##### Example data

Data used in this method comes from the [Supplementary Table 2](https://media.nature.com/original/nature-assets/nbt/journal/v26/n4/extref/nbt1392-S2.xls) of the reference paper. First download it and delete the useless columns. Then, we need add a column `is_liver_metastasis` to indicate whether the patient is a liver metastasis case or not:

```pre
=IF(AND(B2="Liver",C2=1),1,0)
```

Here, column `B` is original `tumor_site` column and `C` is `is_metastatic` column in the table. So if a value in `is_liver_metastasis` column is `1`, the patient should be a liver metastasis case, on the other hand, he/she is not allowed to be classified as originating from liver tissue and were classified to the right branch in node `no. 1` (**see below**).

The column names of the table has no prefix `hsa-`. Saving the table as *csv UTF-8* format with name [`test_data.csv`](./miRNATreeClassifier/test_data.csv), we then used a perl one-liner to modify the column names to make the table be consistent with other descriptions through the story:

```bash
perl -i -F',' -lanE'if($.==1){for(@F){$_=qq{hsa-}.$_ if /-/}say @{[join q{,},@F]}}else{say}' test_data.csv
```

However, the miRNA names in this table don't completely match with **Table 2** in paper, the difference is listed below:

|Table 2 |SI Table|
|-|-
|hsa-miR-145 |	NA
|hsa-miR-92a|	NA
|hsa-miR-21|	NA
|NA	|miR-649
|NA	|miR-661
|NA	|miR-92

To make them consistent, the miRNA names in `test_data.csv` were finally changed:

|SI Table|`test_data.csv`|
|-|-
|miR-649|hsa-miR-21
|miR-661|hsa-miR-145
|miR-92|hsa-miR-92a

> We have contact authors for details about this problem.

Similarly, we saved the [Supplementary Table 3](https://media.nature.com/original/nature-assets/nbt/journal/v26/n4/extref/nbt1392-S3.xls) (emmm, #2 in online version) whose first few lines (those useless lines) were removed as *csv UTF-8* format with name [`model.csv`](./miRNATreeClassifier/model.csv). This table is used as the model for predicting.

The stars (*) labeling hsa-miR-9 in both tables were also be removed.

It is convenient for us to test our script use the modified data.

##### Inputdata preparation

To predict tumor tissue of origin with miRNA, users should prepare their input data similar to our test data, i.e. a data table with "gender" ofthe patients as the first colomn to make sure a higher prediction efficiency of the model, followed by "tumor site" as the second, and then whether the tumor has liver metastasis, that is "is_liver_metastasis" in the third column, "1" represents the patient had a liver metastasis, while "0" the opposite. Other columns of the table contain the detected expression of these 48 miRNAs from this patient. Except for the "tumor site",other items mentioned above are all indispensable for the prediction.

##### How to make prediction?

The method was implemented as Python 3 script [miRNATreeClassifier.py](./miRNATreeClassifier/miRNATreeClassifier.py).

To run the script, first satisfy the environment using `conda env`, then just pass file names to it:

```bash
conda create -n miRNATreeClassifier pandas
conda activate miRNATreeClassifier
./miRNATreeClassifier.py model.csv test_data.csv
```

> Note: `model.csv` is used as a well trained model, should not be changed. 

### For more:

- A post but never published: [The Mystery of the Origin — Cancer Type Classification using Fast.AI Library](https://towardsdatascience.com/the-mystery-of-the-origin-cancer-type-classification-using-fast-ai-libray-212eaf8d3f4e)
- More about TOO: [https://www.cancergenetics.com/laboratory-services/specialty-tests/too-tissue-of-origin-test/]

## Reference

[1]: Pimiento, J.M., Teso, D., Malkan, A., Dudrick, S.J. & Palesty, J.A. Cancer of unknownprimary origin: a decade of experience in a community-based hospital. Am. J. Surg. 194, 833–7, discussion 837–8 (2007).
