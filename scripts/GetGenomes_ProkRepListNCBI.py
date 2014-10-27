#Created on 31/8/14
#Juan A. Ugalde
#juan@ecogenomica.cl

import os
import sys
import fnmatch
import shutil
import subprocess

input_file = sys.argv[1]
output_folder = "selected_genomes"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

failed_genomes = open(output_folder + "/failed_genomes.txt", 'w')
copied_genomes = open(output_folder + "/correct_genomes.txt", 'w')

working_directory = os.getcwd()
species_list = []

for line in open(input_file, 'r'):
    if line.startswith("#"):
        continue

    os.chdir(working_directory)

    line = line.rstrip()
    elements = line.split("\t")
    species_name = "_".join(elements[2].split(" "))

    if int(elements[1]) == 0:
        failed_genomes.write(elements[2] + "\t" + species_name + "\n")
        continue

    #Look for the species name in the bacteria
    #and bacteria_draft folders
    draft = True

    for genome_folder in os.listdir("Bacteria"):
        if fnmatch.fnmatch(genome_folder, species_name + "_uid*"):

            if species_name in species_list:
                continue

            species_output_folder = output_folder + "/" + species_name
            os.mkdir(species_output_folder)

            for files in os.listdir("Bacteria/" + genome_folder + "/"):
                if files.endswith(".fna"):
                    file_path = "Bacteria/" + genome_folder + "/" + files
                    shutil.copy(file_path, species_output_folder)
                    #Check that files were copied
                    if len(os.listdir(species_output_folder)) == 0:
                        os.rmdir(species_output_folder)
                        failed_genomes.write(elements[2] + "\t" + species_name + "\n")
                    else:
                        species_list.append(species_name)
                        copied_genomes.write(elements[2] + "\t" + species_name + "\n")
                        draft = False

    if draft:
        for genome_folder in os.listdir("Bacteria_DRAFT"):
            if fnmatch.fnmatch(genome_folder, species_name + "_uid*"):

                if species_name in species_list:
                    continue

                species_output_folder = output_folder + "/" + species_name
                os.mkdir(species_output_folder)

                for files in os.listdir("Bacteria_DRAFT/" + genome_folder + "/"):
                    if files.endswith(".fna.tgz"):
                        file_path = "Bacteria_DRAFT/" + genome_folder + "/" + files
                        shutil.copy(file_path, species_output_folder)

                        if len(os.listdir(species_output_folder)) == 0:
                            os.rmdir(species_output_folder)
                            failed_genomes.write(elements[2] + "\t" + species_name + "\n")
                        else:
                            species_list.append(species_name)
                            copied_genomes.write(elements[2] + "\t" + species_name + "\n")
                            os.chdir(species_output_folder)
                            subprocess.call(["tar", "-xvf", files])








#TODO:
#Need to check that there are fasta in the folder
#If not, check for gz files, copy those and uncompressed.
#then delete the gz file
