# Code and Data Accompanying the Study "A New Framework for the Representation and Computation of Uncertainty in Phonological Reconstruction"

This repository provides code and data accompanying our study on the representation and computation of uncertainty in phonological reconstruction.

> List, J.-M.; Hill, N. W.; Blum, F.; and Forkel, R. (forthcoming): Representing and Computing Uncertainty in Phonological Reconstruction. To appear in: Proceedings of the 4th Workshop on Computational Approaches to Historical Language Change.

To get started, install all required packages:

```shell
$ pip install -r requirements.txt
```

Having installed all packages, we recommend to first download the data. This can be done with the Makefile we provide:

```shell
$ make download
```

For the individual commands (you will need to have `git` installed), please refer to the Makefile.

To run the analyses for each language, you can again use the Makefile:

```shell
$ make karen
$ make burmish
$ make panoan
```
This will run all analyses and specifically create Markdown and PDF files that show the output of the analyses. All results are also provided here.

The statistics reported in our study can be computed with the following command:

```
$ make stats
```

The result we obtain is:

| Dataset   | Prediction   |   Count |   Proportion |   Alignment Size |
|:----------|:-------------|--------:|-------------:|-----------------:|
| Karen     | correct      |     246 |         0.65 |             4.03 |
| Karen     | false        |     133 |         0.35 |             4.27 |
| Karen     | certain      |     310 |         0.82 |             4.05 |
| Karen     | uncertain    |      69 |         0.18 |             4.41 |
| Burmish   | correct      |     154 |         0.57 |             4.13 |
| Burmish   | false        |     115 |         0.43 |             4.29 |
| Burmish   | certain      |     199 |         0.74 |             4.13 |
| Burmish   | uncertain    |      70 |         0.26 |             4.39 |
| Panoan    | correct      |     405 |         0.79 |             4.25 |
| Panoan    | false        |     109 |         0.21 |             5.14 |
| Panoan    | certain      |     465 |         0.9  |             4.37 |
| Panoan    | uncertain    |      49 |         0.1  |             5.14 |

