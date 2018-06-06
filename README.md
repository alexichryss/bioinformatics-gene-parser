I wanted the focus of my final project to be my 23AndMe data and what I could do with it. After preliminary research, I was able to find a list of disease SNPs. Curious about whether my reported alleles matched with any of the risk alleles I had found, I wrote a program to do the comparison for me.

The programs use data that I gathered and parsed from https://www.eupedia.com/genetics/medical_dna_test.shtml. Thanks to them, I was able to collect several tables worth of disease data, which are provided in the 'data' folder. 

-----------------------------------------------------------------------------------------
Summary - gene-checker.py:
Takes a filename as an argument. The file should be the unpacked text file from 23andMe.

The progress bar will display the program's progress. The entire run takes 2 minutes on average (on an average cpu). Parallelizing the gene search dropped the time from ~4 minutes to 2.

The program uses the python package tqdm to create the progress bar and joblib to handle the pararellization.

Use the example.file as a test; it provides gene matches to demonstrate typical output, while keeping the running time to a minimum. 

Example Output:
['Description', 'SNP', 'Chromosome', 'Genotype', 'Likelihood']
['Glaucoma', 'rs2165241', '15', 'TT', 'Most Likely']
['Glaucoma', 'rs2165242', '16', 'TT', 'Most Likely']
['Glaucoma', 'rs2165243', '17', 'TT', 'Most Likely']

Usage:
$ python gene-checker.py example.file

-----------------------------------------------------------------------------------------
Summary - compare.py:
Used to compare the results of two 23AndMe participants. It returns all the markers for which both participants had identical results.

Usage:
$ python compare.py first.csv second.csv

-----------------------------------------------------------------------------------------
Summary - gene-ratios.py:
Alters the utility of gene-checker.py. Rather than separate each match by line, it sums the results of all alleles found for a disease and returns the aggregate ratios.

Example Output:
Glaucoma (3): {'Most Likely': 1.0}

is returned for the 3 alleles, as opposed to 3 separate lines.

Usage:
$ python gene-ratios.py example.file
