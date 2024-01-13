# EIS1600 Tools

* [Workflow](#workflow)
* [Process](#process)
* [Installation](#installation)
  * [Common Error Messages](#common-error-messages)
* [Set Up](#set-up-virtual-environment-and-install-the-eis1600-pkg-there)
* [Working Directory Structure](#structure-of-the-working-directory)
* [Usage](#usage)
  * [convert_mARkdown_to_EIS1600TMP](#convert-markdown-to-eis1600-files)
  * [insert_uids](#convert-markdown-to-eis1600-files)
  * [update_uids](#convert-markdown-to-eis1600-files)
  * [disassemble_into_miu_files](#disassembling)
  * [reassble-from-miu_files](#reassembling)
  * [annotate_mius](#annotation)
  * [onomastic_annotation](#only-onomastic-annotation)
  * [miu_random_revision](#miu-revision)
  * [yml_to_json](#collect-yamlheaders-into-json)
  * [q_tags_to_bio](#get-training-data-from-q-annotations)

## Workflow

(*so that we do not forget again...*)

1. Double-check text in the Google Spreadsheet; “tag” is as “double-checked” (Column **PREPARED**);
  - These double-checked files have been converted to `*.EIS1600` format
2. The names of these files are then collected into `AUTOREPORT.md` under **DOUBLE-CHECKED Files (XX) - ready for MIU**.
3. Running `disassemble_into_mius` takes the list from `AUTOREPORT.md` and disassembles these files into MIUs and stores them in the MIU repo.

## Process

1. Convert from mARkdown to EIS1600TMP with `convert_mARkdown_to_EIS1600`
2. Check the `.EIS1600TMP`
3. Run `insert_uids` on the checked `.EIS1600TMP`
4. Check again. If anything was changed in the EIS1600 file, run `update_uids`
5. After double-check, the file can be disassembled by `disassemble_into_miu_files <uri_of_that_file>.EIS1600`

## Installation

You can either do the complete local setup and have everything installed on your machine.
Alternatively, you can also use the docker image which can execute all the commands from the EIS1600-pkg.

### Docker Installation

Install Docker Desktop: [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)

It should install Docker Engine as well, which can be used through command line interface (CLI).

To run a script from the EIS1600-pkg with docker, give the command to docker through CLI:
```shell
$ docker run <--gpus all> -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg <EIS1600-pkg-command and its params>
```

Explanation:
* `docker run` starts the image, `-it` propagates CLI input to the image.
* `--gpus all`, optional to run docker with GPUs.
* `-v` will virtualize a directory from your system in the docker image.
* `-v` virtualized `</path/to/EIS1600>` from your system to `/EIS1600` in the docker image. You give the absolute path to our `EIS1600` parent directory on your machine. Make sure to replace `</path/to/EIS1600>` with the correct path on your machine! This is the part in front of the colon, after the colon the destination inside the docker image is specified (this one is fixed).
* `eis1600-pkg` the repository name on docker hub from where the image will be downloaded
* Last, the command from the package you want to execute including all parameters required by that command.

E.G., to run `q_tags_to_bio` for toponym descriptions through docker:
```shell
$ docker run -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg q_tags_to_bio Topo_Data/MIUs/ TOPONYM_DESCRIPTION_DETECTION/toponym_description_training_data TOPD
```

To run the annotation pipeline:
```shell
$ docker run --gpus all -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg analyse_all_on_cluster
```
Maybe add `-D` as parameter to `analyse_all_on_cluster` because parallel processing does not work with GPU.


### Local Setup

After creating and activating the eis16000_env (see [Set Up](#set-up-virtual-environment-and-install-the-eis1600-pkg-there)), use:
```shell
$ pip install eis1600
```

In case you have an older version installed, use:
```shell
$ pip install --upgrade eis1600
```

The package comes with different options, to install camel-tools use the following command.
Check also their installation instructions because atm they require additional packages [https://camel-tools.readthedocs.io/en/latest/getting_started.html#installation](https://camel-tools.readthedocs.io/en/latest/getting_started.html#installation)
```shell
$ pip install 'eis1600[NER]'
```

If you want to run the annotation pipeline, you also need to download camel-tools data:
```shell
$ camel_data -i disambig-mle-calima-msa-r13
```

To run the annotation pipeline with GPU, use this command:

```shell
$ pip install 'eis1600[EIS]'
```

**Note**. You can use `pip freeze` to check the versions of all installed packages, including `eis1600`.

### Common Error Messages

You need to download all the models ONE BY ONE from Google Drive.
Something breaks if you try to download the whole folder, and you get this error:
```shell
OSError: Error no file named pytorch_model.bin, tf_model.h5, model.ckpt.index or flax_model.msgpack found in directory EIS1600_Pretrained_Models/camelbert-ca-finetuned
```
Better to sync `EIS1600_Pretrained_Models` with our nextcloud.

If you want to install `eis1600-pkg` from source you have to add the data modules for `gazetteers` and `helper` manually.
You can find the modules in our nextcloud.

## Set Up Virtual Environment and Install the EIS1600 PKG there

To not mess with other python installations, we recommend installing the package in a virual environment.
To create a new virtual environment with python, run:
```shell
python3 -m venv eis1600_env
```

**NB:** while creating your new virtual environment, you must use Python 3.7 or 3.8, as these are version required by CAMeL-Tools.

After creation of the environment it can be activated by:
```shell
source eis1600_env/bin/activate
```

The environment is now activated and the eis1600 package can be installed into that environment with pip:
```shell
$ pip install eis1600
```
This command installs all dependencies as well, so you should see lots of other libraries being installed. If you do not, you must have used a wrong version of Python while creating your virtual environment.

You can now use the commands listed in this README.

To use the environment, you have to activate it for **every session**, by:
```shell
source eis1600_env/bin/activate
```
After successful activation, your user has the pre-text `(eis1600_env)`.

Probably, you want to create an alias for the source command in your *alias* file by adding the following line:
```shell
alias eis="source eis1600_env/bin/activate"
```

Alias files:

- on Linux:
  - `.bash_aliases`
- On Mac:
  - `.zshrc` if you use `zsh` (default in the latest versions Mac OS);

## Structure of the working directory

The working directory is always the main `EIS1600` directory which is a parent to all the different repositories.
The `EIS1600` directory has the following structure:

```
|
|---| eis_env
|---| EIS1600_MIUs
|---| EIS1600_Pretrained_Models (for annotation, sync from Nextcloud)
|---| gazetteers
|---| Master_Chronicle
|---| OpenITI_EIS1600_Texts
|---| Training_Data
```

Path variables are in the module `eis1600/helper/repo`.

## Usage

### Annotation Pipeline

Use `-D` flag to run annotation of MIUs in sequence, otherwise the annotation will be run in parallel, and it will eat up all resources.
```shell
$ analyse_all_on_cluster
```


### Convert mARkdown to EIS1600 files

Converts mARkdown file to EIS1600TMP (without inserting UIDs).
The .EIS1600TMP file will be created next to the .mARkdown file (you can insert .inProcess or .completed files as well).
This command can be run from anywhere within the text repo - use auto complete (`tab`) to get the correct path to the file.
Alternative: open command line from the folder which contains the file which shall be converted.
```shell
$ convert_mARkdown_to_EIS1600TMP <uri>.mARkdown
```

EIS1600TMP files do not contain UIDs yet, to insert UIDs run insert_uids on the .EIS1600TMP file.
This command can be run from anywhere within the text repo - use auto complete (`tab`) to get the correct path to the file.
```shell
$ insert_uids <uri>.EIS1600TMP
```

#### Batch processing of mARkdown files

Use the `-e` option to process all files from the EIS1600 repo.
```shell
$ convert_mARkdown_to_EIS1600 -e <EIS1600_repo>
$ insert_uids -e <EIS1600_repo>
```

To process all mARkdown files in a directory, give an input AND an output directory.
Resulting .EIS1600TMP files are stored in the output directory.
```shell
$ convert_mARkdown_to_EIS1600 <input_dir> <output_dir>
$ insert_uids <input_dir> <output_dir>
```

### Disassembling

Disassemble files into individual MIU files.
Run from the [parent directory](#structure-of-the-working-directory) `EIS1600`, this will disassemble all files from the `AUTOREPORT`.
```shell
$ disassemble_into_miu_files
```
Can also be run from anywhere within the `EIS1600_MIUs/` directory with a single files as input.
E.G.:
```shell
$ disassemble_into_miu_files <uri_of_the_text>.EIS1600
```

### Reassembling

Run inside MIU repo. Reassemble files into the TEXT repo, therefore, TEXT repo has to be next to MIU repo.
```shell
$ reassemble_from_miu_files <uri>.IDs
```

Use the `-e` option to process all files from the MIU repo. Must be run from the root of MIU repo.
```shell
$ reassemble_from_miu_files -e <MIU_repo>
```

### Annotation

NER annotation for persons, toponyms, misc, and also dates, beginning and ending of onomastic information (*NASAB*), and onomastic information.

**Note** Can only be run if package was installed with *NER* flag AND if the ML models are in the [EIS1600_Pretrained_Models](#structure-of-the-working-directory) directory.

If no input is given, annotation is run for the whole repository. Can be used with `-p` option for parallelization.
Run from the [parent directory](#structure-of-the-working-directory) `EIS1600` (internally used path starts with: `EIS1600_MIUs/`).
```shell
$ annotate_mius -p
```

To annotate all MIU files of a text give the IDs file as argument.
Can be used with `-p` option to run in parallel.
```shell
$ annotate_mius <uri>.IDs
```

To annotate an individual MIU file, give MIU file as argument.
```shell
$ annotate_mius <uri>/MIUs/<uri>.<UID>.EIS1600
```

### Only Onomastic Annotation

**Only for test purposes!**
Can be run with `-D` to process one file at a time, otherwise runs in parallel.
Can be run with `-T` to use gold-standard data as input.
Run from the [parent directory](#structure-of-the-working-directory) `EIS1600`.
```shell
$ onomastic_annotation
```

### Collect YAMLHeaders into JSON

Run from the [parent directory](#structure-of-the-working-directory) `EIS1600`:
```shell
$ yml_to_json
```

### Get training data from Q annotations

This script can be used to transform Q-tags from EIS1600-mARkdown to BIO-labels.
The script will operate on a directory of MIUs and write a JSON file with annotated MIUs in BIO training format.
Parameters are:
1. Path to directory containing annotated MIUs;
2. Filename or path inside RESEARCH_DATA repo for JSON output file
3. BIO_main_class, optional, defaults to 'Q'. Try to use something more meaningful and distinguishable.

```shell
$ q_tags_to_bio <path/to/MIUs/> <q_training_data> <bio_main_class>
```

For toponym definitions/descriptions:
```shell
$ q_tags_to_bio Topo_Data/MIUs/ TOPONYM_DESCRIPTION_DETECTION/toponym_description_training_data TOPD
```

### MIU revision

Run the following command from the root of the MIU repo to revise automated annotated files:
```shell
$ miu_random_revisions
```

When first run, the file *file_picker.yml* is added to the root of the MIU repository.
Make sure to specify your operating system and to set your initials and the path/command to/for Kate in this YAML file.
```yaml
system: ... # options: mac, lin, win;
reviewer: eis1600researcher # change this to your name;
path_to_kate: kate # add absolute path to Kate on your machine; or a working alias (kate should already work)
```
Optional, you can specify a path from where to open files - e.g. if you only want to open training-data, set:
```yaml
miu_main_path: ./training_data/
```

When revising files, remember to change
```yaml
reviewed    : NOT REVIEWED
```
to
```yaml
reviewed    : REVIEWED
```
