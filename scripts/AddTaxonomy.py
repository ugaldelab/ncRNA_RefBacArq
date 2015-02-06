import sys
from Bio import Entrez
import time
from urllib2 import HTTPError


def get_taxid(name):
    """
    Get the taxid for the organism. We need to have this
    to get the full taxonomic lineage
    """
    name = name.replace(" ", "+").strip()
    try:
        search = Entrez.esearch(term=name, db="taxonomy", retmode="xml")
    except HTTPError:
        time.sleep(20)
        search = Entrez.esearch(term=name, db="taxonomy", retmode="xml")
    record = Entrez.read(search)

    return record['IdList'][0]


def get_lineage(id):
    """
    Use the tax ID to get the full lineage record
    """
    try:
        search = Entrez.efetch(id=id, db="taxonomy", retmode="xml")
    except HTTPError:
        time.sleep(20)
        search = Entrez.efetch(id=id, db="taxonomy", retmode="xml")
    record = Entrez.read(search)

    lineage = {d['Rank']: d['ScientificName'] for d in record[0]['LineageEx']}
    return lineage


# def get_tax_data(taxid):
#    """once we have the taxid, we can fetch the record"""
#    search = Entrez.efetch(id=taxid, db="taxonomy", retmode="xml")
#    return Entrez.read(search)


filename = sys.argv[1]

Entrez.email = "juan@ecogenomica.cl"  # Entrez need an email to get the records
if not Entrez.email:
    print "you must add your email address"
    sys.exit(2)

lineage_list = []

#Because of the limit of Entrez, we will work
#in batches

for line in open(filename, 'r'):
    line = line.rstrip()
    if line.startswith("Organism"):
        print "Lineage" + "\t" + line
        continue

    species = line.split("\t")[0]

    taxid = get_taxid(species)
    tax_lineage = get_lineage(taxid)

    lineage_types = ['superkingdom', 'phylum', 'class', 'order',
                     'family', 'genus', 'species']

    lineage_list = []

    for entry in lineage_types:
        if entry in tax_lineage.keys():
            lineage_list.append(tax_lineage[entry])
        else:
            lineage_list.append("unknown")

    print ";".join(lineage_list) + "\t" + line
    time.sleep(1)  # Wait between requests
