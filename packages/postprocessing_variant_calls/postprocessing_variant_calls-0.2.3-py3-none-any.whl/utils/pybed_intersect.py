import pandas as pd
import numpy
import typer
def annotater(maf_df,bed_df,cname):
    """annotates a maf file based on a bed file

    Args:
        maf_df (pandas dataframe): a valid pandas dataframe maf
        bed_df (pandas dataframe): a valid pandas bed file
        cname (string): column name of annotation column

    Returns:
        float: returns maf dataframe with added annotated column
    """
    #TODO break down more
    #sort both the input files
    #TODO handle 0 base case in bedfiles, add a base to bedfile. Maf is 1 based.
    #TODO Do this with an options over commandline: Start_Position + 1, End_Position + 1 for bedfile
    bed_df=bed_df.sort_values(by=['Chromosome', 'Start_Position', 'End_Position'])
    maf_df=maf_df.sort_values(by=['Chromosome', 'Start_Position', 'End_Position'])
    mafdf_sub=maf_df[['Chromosome', 'Start_Position', 'End_Position','Reference_Allele', 'Tumor_Seq_Allele1', 'Tumor_Seq_Allele2']]
    #convert both the files to a dictionary
    mafdf_dic=dict(mafdf_sub.set_index('Chromosome').groupby(level=0).apply(lambda x : x.to_dict(orient='records')))
    beddf_dic=dict(bed_df.set_index('Chromosome').groupby(level=0).apply(lambda x : x.to_dict(orient='records')))
    #loop to process the input files - similar to bedtools intersect
    for k1,v1 in mafdf_dic.items():
        # subset to bed
        subset_bed = beddf_dic[k1]
        # iterate over locations in maf
        for idx, loc_maf in enumerate(v1):
            idb = 0
            found = False
            while found is False and idb <= (len(subset_bed) - 1): 
                loc_bed = subset_bed[idb]
                #TODO take advantage of sorted bed and maf
                # logic for whether to include comment 
                include_logic = (loc_maf['Start_Position'] >= loc_bed['Start_Position']) and (loc_maf['End_Position'] < loc_bed['End_Position']) 
                if include_logic:
                    # add comment to bed 
                    loc_maf[cname] = 'yes'
                    mafdf_dic[k1][idx] = loc_maf
                    found = True 
                if not include_logic: 
                    loc_maf[cname] = 'no' 
                    mafdf_dic[k1][idx] = loc_maf
                idb = idb + 1 
    # combining annotations back into a single dataframe
    maf_annotated = []
    for k1 in mafdf_dic:
        chr_df_maf = pd.DataFrame(mafdf_dic[k1])
        chr_df_maf['Chromosome'] = k1
        maf_annotated.append(chr_df_maf)
    # writing out
    combined_annotations = pd.concat(maf_annotated, axis=0, ignore_index=True)
    final_annotate = combined_annotations.merge(maf_df, on=['Start_Position','End_Position', 'Chromosome','Reference_Allele', 'Tumor_Seq_Allele1', 'Tumor_Seq_Allele2'], how='right')
    sort_index=maf_df.columns.values.tolist()
    sort_index=sort_index+[cname]
    return final_annotate[sort_index]
