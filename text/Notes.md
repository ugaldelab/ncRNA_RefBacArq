#ncRNA in Microbial Genomes

##Genome data
To get the list of representatives prokaryote genomes to use, I downloaded the file from the NCBI repository (8/18/14):

http://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prok_representative_genomes.txt

And I'm using this perl script (https://raw.githubusercontent.com/hyattpd/gbproks/5550c26553fe660ff9b3aad316beec163eb2ed8b/downloadProks.pl) to download all of the ncbi prok genomes. 

Due to speed constrains, I'm doing this on Eider. If needed, I can copy this files to another computer. The idea is to choose the list of prok_representative_genomes, from this downloaded repository (~2400 genomes), and copy this into our local server. These genomes will serve as the basis for further analyses.
http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&rettype=fasta&retmode=text&id=NZ_AFEJ01000001



