gene-checker.py takes a filename as an argument. The file should be the unpacked text file from 23andMe.

The progress bar will display the program's progress. The entire run takes 2 minutes on average. Pararrelizing the gene search dropped the time from ~4 minutes to 2.

The program uses the python package tqdm to create the progress bar and joblib to handle the pararellization.

Use the example.file as a test. Gene matches are provided to demonstrate typical output.

Run as follows:

$ python gene-checker.py example.file
