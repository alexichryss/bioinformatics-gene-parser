import sys
import glob
import os
import csv
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing

DISEASES = []

# class to hold gene information from 23AndMe
class Gene(object):
    def __init__(self, rsid = '', chromosome = '', position = '', genotype = ''):
        self.rsid = rsid
        self.chromosome = chromosome
        self.position = position
        self.genotype = genotype

# class to hold disease gene from csv's
class Disease(object):
    def __init__(self, line):
        elements = [x.strip() for x in line]
        self.description = elements[0]
        genes = []
        self.genes = genes
        self.add_genes(elements)

    # adds genes attribute to a Disease
    def add_genes(self, elements):
        headers = ['Description', 'Chromosome', 'Gene', 'SNP', 'Risk alleles',
                   'Not Likely', 'Less Likely', 'Normal', 'More Likely',
                   'Most Likely', 'Carrier']
        gene = {}
        for i in range(1,len(headers)):
            gene[headers[i]] = elements[i]
        
        self.genes.append(gene)

# takes the filename of a 23AndMe file
def process(filename):
    genes = []
    # reads 23AndMe genes into the genes array
    with open(filename, 'r') as f:
        print('Getting Genome...')
        for line in tqdm(f):
            gene = ''
            if line[0] != '#':
                # rsid chromosome position genotype
                line = line.split()
                gene = Gene(line[0], line[1], line[2], line[3])
                genes.append(gene)
    f.close()

    print('Processing Genome...')
    num_cores = multiprocessing.cpu_count()

    # process genes in parallel
    results = Parallel(n_jobs=num_cores)(delayed(compute)(gene) for gene in tqdm(genes))
    # flatten the results array
    results = [y for x in results for y in x]

    for c in results:
        if 'Carrier' in c:
            print(c)
    for m in results:
        if 'Most Likely' in m:
            print(m)

    # save the results to an output file
    with open('output.txt', 'w+') as s:
        for match in results:
            string = ','.join(match)
            s.write(string + '\n')
    s.close()

# checks if gene exists in DISEASES
def compute(gene):
    matches = []
    for disease in DISEASES:
        for seq in disease.genes:
            if seq['SNP'].strip() == gene.rsid.strip():
                match = []
                match.append(disease.description)
                match.append(seq['SNP'])

                if gene.genotype in seq['Not Likely']:
                    match.append('Not Likely')
                    matches.append(match)
                if gene.genotype in seq['Less Likely']:
                    match.append('Less Likely')
                    matches.append(match)
                if gene.genotype in seq['Normal']:
                    match.append('Normal')
                    matches.append(match)
                if gene.genotype in seq['More Likely']:
                    match.append('More Likely')
                    matches.append(match)
                if gene.genotype in seq['Most Likely']:
                    match.append('Most Likely')
                    matches.append(match)
                if gene.genotype in seq['Carrier']:
                    match.append('Carrier')
                    matches.append(match)
    return matches

# reads in csv file of diseases and passes each line to a build iterator
def set_diseases(filename):
    builder = build()
    builder.send(None)
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spamreader)
        for row in spamreader:
            builder.send(row)
        builder.send(['EOF\n'])
    csvfile.close()

# takes disease gene lines and stores them in a Disease class
def build():
    started = False
    while True:
        line = yield
        if line[0] != '' and not started:
            disease = Disease(line)
            started = True
        elif line[0].strip() == '' and started:
            disease.add_genes(line)
        else:
            global DISEASES
            DISEASES.append(disease)
            if line[0] != 'EOF\n':
                disease = Disease(line)

# takes 23AndMe file and outputs matches to risk alleles
def main():
    
    try:
        args = sys.argv[1]
    except:
        print('Usage: {} <23AndMe filename>'.format(sys.argv[0]))
        return

    print('Processing gene files...')
    for f in tqdm(glob.glob('./data/*.csv')):
        set_diseases(os.path.join('', f))

    try:
        process(args)
    except:
        print('Could not process file')

if __name__ == '__main__':
    main()