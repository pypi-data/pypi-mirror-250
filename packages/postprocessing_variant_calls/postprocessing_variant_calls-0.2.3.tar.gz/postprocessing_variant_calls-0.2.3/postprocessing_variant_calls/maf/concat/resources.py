

# minimal column names
#TODO we'll likely need to adjust in the future.
minimal_maf_columns = [
                "Hugo_Symbol", 
                "Chromosome", 
                "Start_Position", 
                "End_Position", 
                "Reference_Allele", 
                "Tumor_Seq_Allele2", 
                "Variant_Classification", 
                "Variant_Type", 
                "Tumor_Sample_Barcode", 
                "Matched_Norm_Sample_Barcode", 
                "HGVSc",
                "HGVSp",
                "HGVSp_Short",
                "t_ref_count", 
                "t_alt_count", 
                "n_ref_count", 
                "n_alt_count",
]

de_duplication_columns = [
                "Hugo_Symbol", 
                "Chromosome", 
                "Start_Position", 
                "End_Position", 
                "Reference_Allele", 
                "Tumor_Seq_Allele2", 
                "Variant_Classification", 
                "Variant_Type", 
                "HGVSc",
                "HGVSp",
                "HGVSp_Short",
]
acceptable_extensions = ['.maf', '.txt', '.csv', 'tsv']