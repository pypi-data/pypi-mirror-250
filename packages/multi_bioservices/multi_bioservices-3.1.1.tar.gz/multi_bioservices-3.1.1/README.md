# Multi Bioservices

![PyPI - Version](https://img.shields.io/pypi/v/multi_bioservices?style=for-the-badge&logo=PyPy&logoColor=white&color=red)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/JoshLoecker/multi_bioservices/tests.yml?style=for-the-badge&logo=pytest&logoColor=white&label=Tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/multi_bioservices?style=for-the-badge&logo=python&logoColor=white)
![Coveralls branch](https://img.shields.io/coverallsCoverage/github/JoshLoecker/multi_bioservices?branch=master&style=for-the-badge&logo=coveralls&logoColor=white)

## Description

`multi_bioservices` is a utility package for [COMO](https://github.com/HelikarLab/COMO). Its purpose is to provie better
multithreaded access to the [Bioservices](https://bioservices.readthedocs.io/en/master/) package. This is done by
using ThreadPoolExecutors on the synchronous functions. Currently, the only function this package provides is a wrapper
around the `db2db` function in Bioservices.

## Installation

To install `multi_bioservices`, you can use pip:

```bash
pip install multi_bioservices
```

## Usage

To use `multi_bioservices`, simply import the `db2db` function and call it with the relevant parameters

```python
from multi_bioservices.biodbnet import db2db, InputDatabase, OutputDatabase, TaxonID

db2db(
    input_values=["1", "2", "3"],
    input_db=InputDatabase.GENE_ID,
    output_db=OutputDatabase.GENE_SYMBOL,
    taxon_id=TaxonID.HOMO_SAPIENS
)
```

## Parameters

|      Parameter      |                    Type                    | Required? |                                                  Default Value                                                   |                                Description                                |
|:-------------------:|:------------------------------------------:|:---------:|:----------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------:|
|   `input_values`    |                `list[str]`                 |  **Yes**  |                                                       N/A                                                        |                        The input values to convert                        |
|     `input_db`      |              `InputDatabase`               |  **Yes**  |                                                       N/A                                                        |                              The input type                               |
|     `output_db`     | `OutputDatabase` or `list[OutputDatabase]` |    No     | `tuple(OutputDatabase.GENE_SYMBOL.value,OutputDatabase.GENE_ID.value, OutputDatabase.CHROMOSOMAL_LOCATION.value` |                            The type to return                             |
|     `taxon_id`      |             `TaxonID` or `int`             |    No     |                                          `TaxonID.HOMO_SAPIENS` (9606)                                           |                      The taxonomy of the input type                       |
|       `quiet`       |                   `bool`                   |    No     |                                                     `False`                                                      |                     Should all output be suppressed?                      |
| `remove_duplicates` |                   `bool`                   |    No     |                                                     `False`                                                      |         Should duplicates be removed from the returned dataframe?         |
|       `cache`       |                   `bool`                   |    No     |                                                      `True`                                                      |                           Should cache be used?                           |
|       `delay`       |                   `int`                    |    No     |                                                       `5`                                                        | How long of a delay should be enforced if the API is accessed to quickly? |
|    `concurrency`    |                   `int`                    |    No     |                                                   `8` (max 20)                                                   |             How many concurrent requests can be made at once?             |
|   `batch_length`    |                   `int`                    |    No     |                             `300` (max 500 if `taxon_id` is `TaxonID.HOMO_SAPIENS`)                              |                How many items should be converted at once?                |

## Returns

`multi_bioservices` returns a dataframe with the input and output databases as column names. The index of the dataframe
has been reset, starting at 0

An example dataframe is seen below

| Index | Gene ID | Gene Symbol |
|:-----:|:-------:|:-----------:|
|   0   |    0    |      -      |
|   1   |    1    |    A1BG     |
|   2   |    2    |     A2M     |
|   3   |    3    |    A2MP1    |
|   4   |    4    |      -      |

