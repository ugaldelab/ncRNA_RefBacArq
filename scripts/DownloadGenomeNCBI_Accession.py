#!/Users/jugalde/anaconda/bin/python
# Created on 18/8/14
# Juan A. Ugalde
# juan@ecogenomica.cl
#Inspiration on some of the Antismash2 code
#https://searchcode.com/codesearch/view/46100471/

import time
from cogent.db.ncbi import EUtils
from Bio import SeqIO
import re
import argparse
import os

WGS_project = re.compile("N[A-Z]_[a-zA-Z]{4,6}\d{8,10}")

def check_WGS_project(sequence_id):
    check = WGS_project.match(sequence_id)
    if check:
        isWGS = True
    else:
        isWGS = False
    return isWGS

def get_fasta_sequence(sequence_id, output_folder):
    e = EUtils(db="nucleotide", rettype="fasta")
    outfile = open(output_folder + "/fasta/" + sequence_id + ".fasta",'a')
    outfile.write(e[sequence_id].read())
    outfile.close()

def get_wgs_gb(sequence_id, output_folder):
    e = EUtils(db="nucleotide", rettype="gb")
    outfile = open(output_folder + "/wgs_gb/" + sequence_id + ".gb",'w')
    outfile.write(e[sequence_id].read())
    outfile.close()

def parse_wgs_gb(gb_file):
    contig_list = []
    wgs_record = SeqIO.read(gb_file, 'genbank')
    print wgs_record.annotations['wgs_scafld']


program_description = "This script downloads a list of genomes from NCBI using\
                       their accession numbers. The required file is the list of\
                       prokaryote representative genomes."

parser = argparse.ArgumentParser(description = program_description)

parser.add_argument("-l", "--ncbi_prok_file", type=str, help="NCBI prok file",
                    required=True)
parser.add_argument("-o", "--output_folder", type=str, help="Output Folder",
                    required=True)

args = parser.parse_args()

#Read the genome list, and iterate over each entry. Download genbank file
i = 1

#Create output folder
if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)
    os.makedirs(args.output_folder + "/fasta")
    os.makedirs(args.output_folder + "/wgs_gb")


for line in open(args.ncbi_prok_file, 'r'):
    line = line.rstrip()
    elements = line.split("\t")

    species_name = elements[2]
    accesion_number = elements[3]

    if check_WGS_project(accesion_number) is False:
    #    get_fasta_sequence(accesion_number, args.output_folder)
    #    time.sleep(5)
        continue

    else:
        parse_wgs_gb("test.txt")

    print accesion_number, check_WGS_project(accesion_number), i
    i += 1
