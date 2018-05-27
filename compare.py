import sys
import glob
import os
import csv

# reads in two csv files and compares gene likelihood
def process(files):
    first = []
    second = []
    matches = []

    with open(files[0], 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spamreader)
        for row in spamreader:
            first.append(row)
    csvfile.close()

    with open(files[1], 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spamreader)
        for row in spamreader:
            second.append(row)
    csvfile.close()

    for f in first:
        for s in second:
            if f == s:
                matches.append(f)

    print('Matches: ')
    for match in matches:
        if match[4] in ['Carrier', 'Most Likely']:
            print(match)
    
     # save the results to an output file
    i = 0
    path = 'matches_' + str(i) + '.txt'
    header = ['Description', 'SNP', 'Chromosome', 'Genotype', 'Likelihood']
    while os.path.isfile(path):
        i += 1
        path = 'output_' + str(i) + '.txt'
    with open(path, 'w+') as s:
        s.write('Matches:\n')
        header = ','.join(header)
        s.write(header + '\n')
        for match in matches:
            match[0] = '"' + match[0] + '"'
            string = ','.join(match)
            s.write(string + '\n')
    s.close()

# takes two csv files and outputs matches
def main():
    
    try:
        args = sys.argv[1:]
    except:
        print('Usage: {} <1st csv file> <2nd csv file>'.format(sys.argv[0]))
        return

    try:
        process(args)
    except:
        print('Could not process file')

if __name__ == '__main__':
    main()