#!/usr/bin/env python
# imports
import os
import sys
import csv 
import typer
class maf_annotater():
    '''
    @Description : The purpose of this class is to manage the variety of information specified about a vardict as well as 
                    manage filtering one with both single and double sample 
    @Created : 04/20/2022
    @author : Karthigayini Sivaprakasam, Eric Buehler 
    -init: 
        -inputVcf
        -sampleName 
        -minQual 
        -totalDepth 
        -alleleDepth 
        -variantFraction
        -tnRatio 
        -filterGermline
        -outputDir
        -vcf_out
        -allsamples
        -vcf_reader
        -vcf_complex_out
        -txt_out
    ''' 
    def __init__(self, input_maf, hotspot_maf, output_maf):
        self.input_maf = input_maf
        self.hotspot_maf = hotspot_maf
        self.output_maf = output_maf
        # Use these fields to uniquely identify each mutation
        self.MUTATION_KEYS = [
            'Chromosome',
            'Start_Position',
            'Reference_Allele',
            'Tumor_Seq_Allele2'
        ]

    def tag_hotspots(self):
        
                # Load hotspots into a set for easy lookup by chr:pos:ref:alt, and store AA position changed
        hotspots = set()
        with open(self.hotspot_maf, 'r') as infile:
            reader = csv.DictReader(infile, delimiter='\t')
            for row in reader:
                key = ':'.join([row[k] for k in self.MUTATION_KEYS])
                hotspots.add(tuple(key))

        # Parse through input MAF, and create a new one with an extra column tagging hotspots
        with open(self.input_maf, 'r') as infile:
            with open(self.output_maf, 'w') as outfile:

                # Todo: Comment lines are tossed, though they may need to be retained in some use cases
                filtered_rows = (row for row in infile if not row.startswith('#'))
                reader = csv.DictReader(filtered_rows, delimiter='\t')
                writer = csv.DictWriter(outfile, delimiter='\t', lineterminator='\n', fieldnames=reader.fieldnames + ["hotspot_whitelist"])
                writer.writeheader()

                for row in reader:
                    row['hotspot_whitelist'] = 'FALSE'
                    key = ':'.join([row[k] for k in self.MUTATION_KEYS])
                    if tuple(key) in hotspots:
                        row['hotspot_whitelist'] = 'TRUE'
                    writer.writerow(row)

