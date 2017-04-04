# Batches

  * [Introduction](#introduction)
  * [Manipulating Batches](#manipulating-batches)
    + [Creating a Batch](#creating-a-batch)
    + [Creating a Batch for Re-analysis](#creating-a-batch-for-re-analysis)
    + [Adding More Samples](#adding-more-samples)
    + [Viewing Batch Information](#viewing-batch-information)
  * [Files](#files)
    + [Data Directory](#data-directory)
    + [Sample Metadata](#sample-metadata)
      - [Abbreviations](#abbreviations)
    + [config.batch.groovy](#configbatchgroovy)
    
## Introduction
In Cpipe, a batch is a group of samples to be analysed at the same time. In the filesystem, a batch is a directory inside
 `cpipe/batches`. For example, a batch named `batch_001` would mean creating a `cpipe/batches/batch_001` directory.
 
## Manipulating Batches
### Creating a Batch
Once you have your fastq files, follow these steps to create a new analysis batch:
* Create the batch directory and copy in the fastq data:
    ```bash
    mkdir -p batches/<batch identifier>/data
    cp <fastq files> batches/<batch identifier>/data
    ```
* Create the metadata file using:
   ```bash
  ./cpipe batch add_batch --batch <batch identifier> --profile <profile name> --exome <target region>
   ```
    * `<target region>` is the full filepath to a capture regions bed file specified by your sequencer. For example, for
    Illumina sequencing prepared with a Nextera DNA Library Preparation Kit, this file can be downloaded from 
    [the Illumina website](http://support.illumina.com/downloads/nextera-rapid-capture-exome-v1-2-product-files.html).
    * `<profile name>` is the name of the design (subdirectory within `cpipe/designs`) to use for the analysis. By default
    this is the ALL profile, which we recommend using. See the [designs documentation](designs.md) for more information.

  For more information on the `add_batch` command, refer to its [documentation](commands.md#add-batch)
  
### Creating a Batch for Re-analysis
If you intend to re-analyse an existing batch from an old version of Cpipe, first create the new batch directory, then
copy the data directory, sample metadata file, and config file into this new batch. You can use this script to assist 
you.

First set the `OLD_BATCH` and `NEW_BATCH` variables to the path to the relevant batch directory (e.g. `OLD_BATCH=batches/001`, 
`NEW_BATCH=/path/to/old/cpipe/batches/001`
and then run this script:
```bash
mkdir -p $NEW_BATCH
for file in data/ samples.txt target_regions.txt config.batch.groovy ; do
    if [[ -e $OLD_BATCH/$file ]] ; then
        cp -R $OLD_BATCH/$file $NEW_BATCH
    fi
done
```

Note that you don't need to run the `add_batch` script as you do when creating a new batch, because this creates the
 metadata file and configuration file which should already exist if you are performing reanalysis.
  
### Adding More Samples

To add more samples to an existing batch, use the `./cpipe batch add_samples` command. Refer to 
[its documentation](./commands.md#add-sample)

### Viewing Batch Information

Cpipe provides two utility commands for viewing batch information:
* `./cpipe batch show_batches` lists all the batches in the current installation. Refer to 
[its documentation](commands.md#show-batches) for more information
* `./cpipe batch show_batch --batch <batch name>` will list information about an existing batch. Refer to
[its documentation](commands.md#show-batch) for more information.

## Files
Inside the batch directory (`batches/<batch name>`) are three fundamental elements. All of these must be present and 
are not optional. Here they are covered in more detail.
 * The `data` subdirectory
 * The sample metadata file
 * A `config.batch.groovy` configuration file
  
### Data Directory 
The data directory is a directory named `data` that will hold all of the fastq samples for this batch. 
Each sample in this directory must fit the pattern `<sample id>_<anything>_<lane number>_<read number>.fastq.gz`, for 
example, `00NA12877_Coriell_000_TGx140395_TL140776_L001_R1.fastq.gz`. The components to this filename are as follows
* `sample id` is any unique name for the sample, e.g. `NA12878` in our example
* `anything` of course can be anything produced by the sequencer, in this case `Coriell_000_TGx140395_TL140776` 
* `lane number` must be the letter L followed by the lane number, in this case L001
* `read number` must be the letter R followed by either 1 or 2, the read number, which is `R1` in this example

### Sample Metadata
The sample metadata is the `samples.txt` located in the batch directory (batches/<batch name>) of the batch you're 
running. The file is a TSV (tab-separated text file), where each line corresponds to an input sample. Here you can set
various options about each sample

|Position | Name | Description | Allowed Values | Used for Analysis | Availability | Required |
|---|---|---|---|---|---|---|
|1 | Batch | Identifier for this batch | No underscores | Yes |  2.2+| Yes
|2 | Sample ID | Identifier for this sample | No underscores  | Yes | 2.2+| Yes 
|3 | DNA Tube ID | ID on the tube containing the sample DNA | Unrestricted | No | 2.2+| No
|4 | Sex | The sex of the patient | `Male`, `Female`, `Unknown`, or `other` | Yes | 2.2+| Yes
|5 | DNA Concentration | Concentration of the DNA sample in ng/μL | Numeric | No | 2.2+| No 
|6 | DNA Volume | Volume of the DNA sample in μL | Numeric | No | 2.2+ | No
|7 | DNA Quantity | Mass of the DNA sample in ng | Numeric | No | 2.2+ | No
|8 | DNA Quality | 260/280nm Ratio of the DNA sample | Numeric | No | 2.2+ | No
|9 | DNA Date | Date of DNA extraction | Comma separated list of dates in the format `yyyymmdd` | No | 2.2+| No
|10 | Cohort | Name of the cohort/design that specifies the regions to be analysed in the patient | Any directory in `cpipe/designs` | Yes | 2.2+| Yes
|11 | Sample Type | Whether the sample is of a normal or tumour cell | `Normal` or `Tumour` | Yes | 2.2+| Yes |
|12 | Fastq files | The fastq sequence files corresponding to this sample | Comma separated list of paths to the FASTQ files in the data directory. | Yes | 2.2+| Yes
|13 | Prioritised genes | The categories are used to prioritise variants from these genes in the gene priority column of the pipeline output | Groups of priorities, each separated by a space. Each group consists of a priority (1-5, where 5 is highest priority), a colon, and then a comma separated list of HGNC symbols. e.g. `3:GABRD,KCNAB2,ALG6 4:CASQ2,HAX1,CHRNB2,KCNJ10` | Yes | 2.2+ | No
|14 | Consanguinity | Extent of consanguinity in the family of the patient | `No`, `Yes`, `Suspected`, or `Unknown` | No | 2.2+ | No
|15 | Variants file | Known variants for the disease | Valid file path | No | 2.2+ | No
|16 | Pedigree file | PED specification for trios (see Trio Analysis below) | Either `import` if you want to use an existing PED file, `exclude` if you want to exclude this from trio analysis, a string of the form `familyId=motherId,fatherId`, where motherId and fatherID are sampleIDs in this metadata file | Yes | 2.2+| No
|17 | Ethnicity | Ethnicity of the patient | `Unknown`, `European`, `African`, or `Asian` | No | 2.2+ | No
|18 | Variant call group | Samples to call as a group e.g. joint calling for related individuals | Comma separated list of sample IDs | No | 2.2+ | No
|19 | Capture date | Date of exome library capture (only relevant for exome sequencing or panels) | Comma separated list of dates of the format  `yyyymmdd` | No | 2.2+ | No
|20 | Sequencing Date | Date of sequencing | Comma separated list of dates in the format `yyyymmdd`| No | 2.2+ | No
|21 | Mean Coverage | Mean coverage of all on-target aligned reads after duplicate removal as obtained by the sequencing laboratory | Numeric| No | 2.2+ | No
|22 | Duplicate Percentage | Percentage of detected duplicates removed before calculating mean on-target coverage | Numeric | No | 2.2+ | No
|23 | Machine ID | ID of the sequencer, provided by the sequencing laboratory | Comma separated list | No | 2.2+ | No
|24 | DNA Extraction Lab | Lab that extracted the DNA | For Melbourne Genomics, this has to be one of the : `RMH`, `MH`, `PMCC`, `AH`, `VCGS`, `CTP`, or `Coriell`. Refer to the [abbreviations list](#abbreviations) below. Otherwise this is unrestricted. | No | 2.2+ | No
|25 | Sequencing Lab | Lab that sequenced the sample | For Melbourne Genomics, must be one of: `PMCC`, `AGRF`, `MH`, or `VCGS`. Refer to the [abbreviations list](#abbreviations) below. Otherwise this is unrestricted. | No | 2.2+ | No
|26 | Exome capture | Capture kit used, including version (e.g. Nextera Rapid Capture Exome 1.2) | Unrestricted | No | 2.2+ | No
|27 | Library preparation | Additional steps involved in library preparation | Unrestricted | No | 2.2+ | No
|28 | Barcode pool size | Number of barcode adapters in the barcode pool | Numeric | No | 2.2+ | No
|29 | Read type | Read length and type | The read length (bp), followed by the type of read (`SE` for single end or `PE` for paired end). e.g. `100PE` | No | 2.2+ | No
|30 | Machine type | Sequencing machine including model (e.g. HiSeq 2500) | Unrestricted | No | 2.2+ | No
|31 | Sequencing chemistry | Chemistry used by the sequencing machine e.g. TruSeq Rapid XPS | Unrestricted | No | 2.2+ | No
|32 | Sequencing software | Software used to generate sequences from the sequencing machine e.g. Illumina RTA 1.18.64 | Unrestricted | No | 2.2+ | No 
|33 | Demultiplex software | <INCLUDE VERSION> e.g. bcl2fastq 1.8.4 | Unrestricted | No | 2.2+| No
|34 | Hospital centre | Origin of the patient sample | For Melbourne Genomics, one of `RMH`, `PMCC`, `RCH`, `AH`, or `MH`. Refer to the [abbreviations list](#abbreviations) below. Otherwise this is unrestricted. | No | 2.2+ | No
|35 | Sequencing contact | Email address to which sequencing alerts should be sent | Valid email | No | 2.2+ | No
|36 | Pipeline contact | Email address where pipeline result alerts should be sent | Unrestricted | No | 2.2+ | No
|37 | Notes | Additional notes or relevant information about the sequencing | Unrestricted | No | 2.2+ | No

#### Abbreviations
The abbreviations listed above in the metadata file correspond to the following laboratories, hospitals and institutes:

Institute | Abbreviation
--- | ---
Royal Melbourne Hospital | RMH
Monash Health | MH
Peter MacCallum Cancer Centre | PMCC
Austin Health | AH
Royal Children's Hospital | RCH
Victorian Clinical Genetics Services | VCGS
Australian Genome Research Facility | AGRF
Centre for Translational Pathology | CTP
Coriell Institute for Medical Research | Coriell

### config.batch.groovy
The final file that must be included in the batch directory is the configuration file. Refer to the [configuration](configuration.md)
section for more details.

Note that, while most of the fields are optional in this file, the config.batch.groovy **must** contain an `EXOME_TARGET`
field. This should be set automatically by running `./cpipe batch add_batch` as documented in the [Creating a Batch](#creating-a-batch)
section.