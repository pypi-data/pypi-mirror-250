#!/usr/bin/env python
# imports
import os
import sys
import csv 
import pandas as pd
import numpy as np 
from utils.pybed_intersect import annotater
import typer


# this function is no longer used
# functionality split up between annoate_process mafbybed and other helpers in this file
def maf_bed_annotate(maf,bed,cname,outputFile):
    """main function for annotation a bed file

    Args:
        maf (string/path): a valid maf file
        bed (string/path): a valid bed file
        cname (string): column name of annotation column
        outputFile (string): name of output file

    Returns:
        float: returns zero if annotated maf successfully written
    """
    ## input files preprocessing
    # call the function to remove lines starting with #
    skip = get_row(maf)
    #read MSF file using Pandas
    maf_df = pd.read_csv(maf, sep="\t", skiprows=skip, low_memory=False)
    #call the function to remove lines starting with #
    skip = get_row(bed)
    #assigning column names to BED file
    bed_names=['Chromosome','Start_Position','End_Position','Comment']
    #store it as Pandas dataframe
    bed_df = pd.read_csv(bed, sep="\t", skiprows=skip, low_memory=False,header=None,names=bed_names)
    #remove the string "chr"
    bed_df['Chromosome']=bed_df['Chromosome'].str.replace("chr", "")
    # annotate maf with processed bed file
    annotated_maf = annotater(maf_df,bed_df,cname)
    # write to csv
    typer.secho(f"Writing out maf file to the following location: {outputFile}.csv".format(outputFile=outputFile), fg=typer.colors.GREEN)
    annotated_maf.to_csv(f"{outputFile}.csv".format(outputFile=outputFile), index=False)
    return 0

def get_row(file):
    skipped = []
    with open(file, "r") as csv_file:
        skipped.extend(i for i, line in enumerate(csv_file) if line.startswith("#"))
    return skipped

def read_bed(bed):
    #call the function to remove lines starting with #
    #assigning column names to BED file
    #store it as Pandas dataframe 
    skip = get_row(bed)
    #TODO more robust handling for bed column names
    bed_names=['Chromosome','Start_Position','End_Position','Comment']
    bed_df = pd.read_csv(bed, sep="\t", skiprows=skip, low_memory=False,header=None,names=bed_names)
    #remove the string "chr"
    bed_df['Chromosome']=bed_df['Chromosome'].str.replace("chr", "")
    return bed_df

def read_maf(maf):
    # call the function to remove lines starting with #
    #read MSF file using Pandas
    skip = get_row(maf)
    maf_df = pd.read_csv(maf, sep="\t", skiprows=skip, low_memory=False)
    return maf_df