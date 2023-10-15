# Code and Data Accompanying the Study "A New Framework for the Representation and Computation of Uncertainty in Phonological Reconstruction"

This repository provides code and data accompanying our study on the representation and computation of uncertainty in phonological reconstruction.

> List, J.-M.; Hill, N. W.; Blum, F.; and Forkel, R. (forthcoming): A New Framework for the Representation and Computation of Uncertainty in Phonological Reconstruction. To appear in: Proceedings of the 4th Workshop on Computational Approaches to Historical Language Change.

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
