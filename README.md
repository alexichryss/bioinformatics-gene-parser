gene-checker.py takes a filename as an argument. The file should be the unpacked text file from 23andMe.

The progress bar will display the program's progress. The entire run takes 2 minutes on average. Pararrelizing the gene search dropped the time from ~4 minutes to 2.

The program uses the python package tqdm to create the progress bar and joblib to handle the pararellization.

Use the example.file as a test. Gene matches are provided to demonstrate typical output.

Run as follows:
$ python gene-checker.py example.file

compare.py is used to compare the results of two 23AndMe participants. It returns all the markers for which both participants had identical results.

Usage:
$ python compare.py first.csv second.csv

gene-ratios.py alters the utility of gene-checker.py. Rather than separate each match by line, it sums the results of all alleles found for a disease and returns the aggregate ratios.

example:
Age-related Macular Degeneration: {'Most Likely': 0.14, 'More Likely': 0.57, 'Normal': 0.29}

is returned for the 12 alleles, as opposed to 12 separate lines.

Usage:
$ python gene-ratios.py example.file
