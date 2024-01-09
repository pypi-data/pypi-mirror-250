#!/usr/bin/env python
# imports
import os
import sys
import csv

from pathlib import Path
from typing import List, Optional
import typer
import pandas as pd
import numpy as np
from postprocessing_variant_calls.maf.concat import acceptable_extensions
from .resources import tsg_genes

def check_maf(files: List[Path]):
    # return non if argument is empty
    if files is None:
        return None
    # check that we have a list of mafs after reading off the cli
    extensions = [os.path.splitext(f)[1] for f in files]
    for ext in extensions:
        if ext not in acceptable_extensions:
            typer.secho(f"If using files argument, all files must be mafs using the same extension.", fg=typer.colors.RED)
            raise typer.Abort()
    return files

def check_txt(paths: Path):
    # return None if argument is empty, kind of unfortunate we have to handle this case
    if paths is None:
        return None
    # check that we have a text file after reading off the cli
    extension = os.path.splitext(paths)[1]
    if extension != '.txt':
        typer.secho(f"If using paths argument, must provided an input txt file.", fg=typer.colors.RED)
        raise typer.Abort()
    return paths

def check_separator(separator: str):
    separator_dict = {"tsv":'\t', "csv":","}
    if separator in separator_dict.keys():
        sep = separator_dict[separator]
    else:
        typer.secho(f"Separator for delimited file must be 'tsv' or 'csv', not '{separator}'", fg=typer.colors.RED)
        raise typer.Abort()
    return sep

def read_tsv(tsv, separator):
    """Read a tsv file

    Args:
        maf (File): Input MAF/tsv like format file

    Returns:
        data_frame: Output a data frame containing the MAF/tsv
    """
    typer.echo("Read Delimited file...")
    skip = get_row(tsv)
    return pd.read_csv(tsv, sep=separator, skiprows=skip, low_memory=True)


def get_row(tsv_file):
    """Function to skip rows

    Args:
        tsv_file (file): file to be read

    Returns:
        list: lines to be skipped
    """
    skipped = []
    with open(tsv_file, "r") as FH:
        skipped.extend(i for i, line in enumerate(FH) if line.startswith("#"))
    return skipped


def gen_id_tsv(df):
    cols = ["Chromosome","Start_Position","End_Position","Reference_Allele","Tumor_Seq_Allele2"]
    if set(cols).issubset(set(df.columns.tolist())):
        df['id'] = df[cols].apply(lambda x: '_'.join(x.replace("-","").astype(str)),axis=1)
    else:
        typer.secho(f"tsv file must include {cols} columns to generate an id for annotating the input maf.", fg=typer.colors.RED)
        raise typer.Abort()
    return df

    
class MAFFile:
    def __init__(self, file_path, separator):
        self.file_path = file_path
        self.separator = separator
        self.data_frame = self.read_tsv()
        self.cols = {
            "general": ["Chromosome","Start_Position","End_Position","Reference_Allele","Tumor_Seq_Allele2"],
            "germline_status": ["t_alt_count", "t_depth"],
            "common_variant": ["gnomAD_AF"],
            "prevalence_in_cosmicDB": ["CNT"],
            "truncating_mut_in_TSG": ["Consequence","Variant_Classification","Hugo_Symbol"],
            "hotspot": ["t_alt_count","hotspot"],
            "non_hotspot": ["t_alt_count","hotspot"],
            "not_complex": ["complexity"],
            "mappable": ["mappability"],
            "non_common_variant" :["common_variant"],
            "cmo_ch_filter": ["t_alt_count", "t_depth","gnomAD_AF","Consequence","Variant_Classification","Hugo_Symbol",
            "t_alt_count","hotspot","t_alt_count","complexity","mappability",
            "Chromosome","Start_Position","End_Position","Reference_Allele","Tumor_Seq_Allele2"]
        }
        self.gen_id()
        self.tsg_genes = tsg_genes
    def read_tsv(self):
        """Read the tsv file and store it in the instance variable 'data_frame'.

        Args: 
            self

        Returns:
            pd.DataFrame: Output a data frame containing the MAF/tsv
        """
        typer.echo("Read Delimited file...")
        skip = self.get_row()
        return pd.read_csv(self.file_path, sep=self.separator, skiprows=skip, low_memory=True)

    def get_row(self):
        """Function to skip rows

        Returns:
            list: lines to be skipped
        """
        skipped = []
        with open(self.file_path, "r") as FH:
            skipped.extend(i for i, line in enumerate(FH) if line.startswith("#"))
        return skipped
    
    def merge(self,maf,id,how):
        maf_df=self.data_frame.merge(maf, on=id, how=how)
        return maf_df
    
    def gen_id(self):
        #TODO need to add better controls for values inputs
        #TODO need to check that column can be found in both mafs 
        cols = ["Chromosome","Start_Position","End_Position","Reference_Allele","Tumor_Seq_Allele2"]
        if set(cols).issubset(set(self.data_frame.columns.tolist())):
            self.data_frame['id'] = self.data_frame[cols].apply(lambda x: '_'.join(x.replace("-","").astype(str)),axis=1)
        else:
            typer.secho(f"maf file must include {cols} columns to generate an id for annotating the input maf.", fg=typer.colors.RED)
            raise typer.Abort()
    
    def annotate_maf_maf(self,maf_df_a,cname,values):
        #TODO need to add better controls for values inputs
        #TODO need to check that column can be found in both mafs 
        self.data_frame[cname] = np.where(self.data_frame["id"].isin(maf_df_a["id"]),values[0],values[1])
        return self.data_frame
    
    def tag(self,tagging):
        cols = self.cols[tagging]
        if set(cols).issubset(set(self.data_frame.columns.tolist())):
            if tagging == "germline_status":
                    self.data_frame['t_alt_freq']= pd.to_numeric((self.data_frame['t_alt_count'])) / pd.to_numeric(self.data_frame['t_depth'])
                    self.data_frame['germline_status']=np.where((self.data_frame['t_alt_freq']>0.35),'likely_germline',"")
            if tagging == "common_variant":
                    self.data_frame['gnomAD_AF']= pd.to_numeric(self.data_frame['gnomAD_AF'])
                    self.data_frame['common_variant']=np.where((self.data_frame['gnomAD_AF']>0.05),'yes','no')
            if tagging == "prevalence_in_cosmicDB":
                    self.data_frame['prevalence_in_cosmicDB']= self.data_frame['CNT'].apply(lambda x: int(x.split(",")[0]) if pd.notnull(x) else x)
                    self.data_frame.drop(['CNT'], axis=1, inplace=True)
            if tagging == "truncating_mut_in_TSG":
                    self.data_frame['truncating_mutation']=np.where((self.data_frame['Consequence'].str.contains("stop_gained")) | (self.data_frame['Variant_Classification']=="Frame_Shift_Ins") | 
        (self.data_frame['Variant_Classification']=="Nonsense_Mutation") | (self.data_frame['Variant_Classification']=="Splice_Site") | (self.data_frame['Variant_Classification']=="Frame_Shift_Del") |
        (self.data_frame['Variant_Classification']=="Translation_Start_Site"),"yes","no")
                    self.data_frame['tumor_suppressor_gene']=np.where(self.data_frame['Hugo_Symbol'].isin(self.tsg_genes),"yes","no")
                    self.data_frame['truncating_mut_in_TSG']= np.where(((self.data_frame['tumor_suppressor_gene']=="yes") & (self.data_frame['truncating_mutation']=="yes")),"yes","no")          
        else:
            typer.secho(f"missing columns expected for {tagging} tagging expects: {set(cols).difference(set(self.data_frame.columns.tolist()))}, which was missing from the input", fg=typer.colors.RED)
            raise typer.Abort()
        return self.data_frame
    
    def tag_all(self,tagging):
        if tagging == "cmo_ch_tag":
            self.tag("germline_status")
            self.tag("common_variant")
            self.tag("prevalence_in_cosmicDB")
            self.tag("truncating_mut_in_TSG")
        return self.data_frame
    
    def filter(self,filter):
        cols = self.cols[filter]
        if set(cols).issubset(set(self.data_frame.columns.tolist())):
            if filter == "hotspot":
                self.data_frame['t_alt_count']=pd.to_numeric(self.data_frame['t_alt_count'])
                self.data_frame['hotspot_retain']=np.where(((self.data_frame['hotspot']=="yes") & (self.data_frame['t_alt_count']>=3)),"yes","no") 
                self.data_frame=self.data_frame[self.data_frame['hotspot_retain']=="yes"]
            if filter == "non_hotspot":
                self.data_frame['t_alt_count']=pd.to_numeric(self.data_frame['t_alt_count'])
                self.data_frame['non_hotspot_retain']=np.where(((self.data_frame['hotspot']=="no") & (self.data_frame['t_alt_count']>=5)),"yes","no") 
                self.data_frame=self.data_frame[self.data_frame['non_hotspot_retain']=="yes"]
            if filter == "not_complex":
                self.data_frame=self.data_frame[self.data_frame['complexity']=="no"]
            if filter == "mappable":
                self.data_frame=self.data_frame[self.data_frame['mappability']=="no"]
            if filter == "non_common_variant":
                self.data_frame=self.data_frame[self.data_frame['common_variant']=="no"]
            if filter == "cmo_ch_filter":
                self.data_frame['retain']=np.where((((self.data_frame['hotspot']=="yes") & (self.data_frame['t_alt_count']>=3)) | ((self.data_frame['hotspot']=="no") & (self.data_frame['t_alt_count']>=5))),"yes","no") 
                self.data_frame=self.data_frame[((self.data_frame['common_variant']=="yes")  & (self.data_frame['mappability']=="no") & (self.data_frame['complexity']=="no") & (self.data_frame['retain']=="yes"))]
        else:
            typer.secho(f"missing columns expected for {filter} filtering expects: {set(cols).difference(set(self.data_frame.columns.tolist()))}, which was missing from the input", fg=typer.colors.RED)
            raise typer.Abort()
        return self.data_frame

