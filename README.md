# prefixrun

A micropackage that runs all of the files in a directory with a prefix of <integer>- in the order of their integer prefixes. This is a simple, straightforward way to create data analysis pipelines. For example, imagine that we have a directory with the following files:

```bash
1-transfer_data.sh
2-build_tables.hql
3-pull_ingest.py
4-model.py
5-visualize_present.R
myproject.py
random.txt
image.jpeg
```

`prefixrun` will take those first 5 files, the ones with integer prefixes, and run them in order of those prefixes, so first `1-transfer_data.sh` is run, then `2-build_tables.hql`, and so on until we finally run `5-visualize_present.R`. This is equivalent to

```bash
bash 1-transfer_data.sh
hive -f 2-build_tables.hql
python 3-pull_ingest.py
python 4-model.py
Rscript 5-visualize_present.R
```

## Installation

```
pip install prefixrun
```

## Useage

`prefixrun` has both a command-line utility, `prefixrun`, and a simple Python API.

### Command-line utility

The command-line utility called `prefixrun` will be installed and added to your system's PATH. See its arguments with `prefixrun --help`.

Simply running the command with no arguments will sequentially run all of the files in the current folder with a prefix of <integer>-. Also available are the following arguments:

- `--directory` : what directory do you want to run prefixed files in?

### Python API

Use the `PrefixRun` class to run prefixed files. By default it looks for files in the current working directory. Use the `directory` argument to switch to a different directory. 

```
from prefixrun import PrefixRun
```

## Default extensions

The following default extensions are provided. You may also specify your own. Please feel free to reach out with suggestions for extensions to add to this list.

```python
{
    '.hql' : ['hive', '-f'],
    '.py' : ['python'],
    '.R' : ['Rscript'],
    '.scala': ['scala'],
    '.sh' : ['bash']
}
```
