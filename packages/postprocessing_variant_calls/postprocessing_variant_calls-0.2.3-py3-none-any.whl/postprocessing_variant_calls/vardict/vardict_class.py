#!/usr/bin/env python
# imports
import os
import sys
import vcf
from vcf.parser import _Info as VcfInfo, _Format as VcfFormat, _vcf_metadata_parser as VcfMetadataParser

class var_sample:
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
    def __init__(self, inputVcf, outputDir, sampleName, minQual, totalDepth, 
                alleleDepth, variantFraction, tnRatio, filterGermline):

        # specified by CLI tool 
        self.inputVcf = inputVcf
        self.outputDir = outputDir
        self.sampleName = sampleName 
        self.minQual = minQual
        self.totalDepth = totalDepth
        self.alleleDepth = alleleDepth
        self.variantFraction = variantFraction
        self.tnRatio = tnRatio
        self.filterGermline = filterGermline
        # custom info 
        # vcf output name
        self.vcf_out = self.out_name()
        self.txt_out = self.vcf_out + "_STDfilter.txt" 
        self.vcf_complex_out = self.vcf_out + "_STDfilter_complex.vcf"
        self.vcf_out = self.vcf_out + "_STDfilter.vcf"
        # vcf reader 
        self.vcf_reader = self.set_reader() 
        # sample list 
        self.allsamples = list(self.vcf_reader.samples)

    def out_name(self):
        '''
        @Description : The purpose of this function is to define the output name of the vcf file 
        @Created : 04/20/2022
        @author : Karthigayini Sivaprakasam, Eric Buehler 
        -input: self 
        -ouput: a string that specifies the name of the output vcf 
        '''
        vcf_out = os.path.basename(self.inputVcf)
        vcf_out = os.path.splitext(vcf_out)[0]
        if self.outputDir != "":
            vcf_out = os.path.join(self.outputDir, vcf_out)
        return vcf_out


    def set_reader(self):  
        # TODO: I probably need to dig a little deeper to see if everything here is still required 
        '''
        @Description : The purpose of this function is to define and set-up a vcf reader
        @Created : 04/20/2022
        @author : Karthigayini Sivaprakasam, Eric Buehler 
        -input: self 
        -ouput: a vcf reader
        '''
        vcf_reader = vcf.Reader(open(self.inputVcf, "r"))
        vcf_reader.infos["set"] = VcfInfo(
            "set",
            ".",
            "String",
            "The variant callers that reported this event",
            "msk-access/postprocessing_varaint_calls",
            "v0.0.1",
            "vcf",
        )
        vcf_reader.formats["DP"] = VcfFormat(
            "DP", "1", "Integer", "Total read depth at this site",
            "vcf",
        )
        vcf_reader.formats["AD"] = VcfFormat(
            "AD",
            "R",
            "Integer",
            "Allelic depths for the ref and alt alleles in the order listed",
            "vcf",
        )

        # Manually add the new SHIFT3_ADJUSTED header to the reader, which will then be passed to the writer
        shift3_line = '##INFO=<ID=SHIFT3_ADJUSTED,Number=1,Type=Integer,Description="No. of bases to be shifted to 5 prime for complex variants to get the preferred left alignment for proper genotyping">'
        meta_parser = VcfMetadataParser()
        key, val = meta_parser.read_info(shift3_line)
        vcf_reader.infos[key] = val
        return vcf_reader 

    def has_normal(self):
        '''
        @Description : The purpose of this function is to check if a normal sample is present
        @Created : 04/20/2022
        @author : Karthigayini Sivaprakasam, Eric Buehler 
        -input: self 
        -ouput: boolean representing whether a normal sample is present or not
        '''
        #TODO there might be more checks we want to add here 
        if len(self.allsamples) == 1:
            return False  
        else: 
            return True

    def filter_single(self):
        # TODO: contiue work on method, check with Karthi / Ronak about single filter  
        '''
        @Description : The purpose of this function is to filter VCFs output from vardict that contain control sample info 
        @Created : 04/20/2022
        @author : Karthigayini Sivaprakasam, Eric Buehler 
        -input: self 
        -ouput: 
            - self.vcf_out
            - self.vcf_complex_out
            - self.txt_out
        '''
        vcf_writer = vcf.Writer(open(self.vcf_out, "w"), self.vcf_reader)
        vcf_complex_writer = vcf.Writer(open(self.vcf_complex_out, "w"), self.vcf_reader)
        txt_fh = open(self.txt_out, "wb")

        # mutations 

        # Iterate through rows and filter mutations
        for record in self.vcf_reader:
            tcall = record.genotype(self.sampleName)

            # Pad complex indels for proper genotyping
            if (
                record.INFO["TYPE"] == "Complex"
                and len(record.REF) != len(record.ALT)
                and record.INFO["SHIFT3"] > 0
                and record.INFO["SHIFT3"] <= len(record.INFO["LSEQ"])
            ):
                padding_seq = record.INFO["LSEQ"][
                    len(record.INFO["LSEQ"]) - (record.INFO["SHIFT3"] + 1) :
                ]
                record.REF = padding_seq + record.REF
                for alt in record.ALT:
                    alt.sequence = padding_seq + alt.sequence
                record.POS = record.POS - (record.INFO["SHIFT3"] + 1)
                record.INFO["SHIFT3_ADJUSTED"] = record.INFO["SHIFT3"]
                record.INFO["SHIFT3"] = 0
                complex_flag = True
            else:
                complex_flag = False
                record.INFO["SHIFT3_ADJUSTED"] = 0

            tmq = int(record.INFO["QUAL"])

            if tcall["DP"] is not None:
                tdp = int(tcall["DP"][0])
            else:
                tdp = 0
            if tcall["VD"] is not None:
                tad = int(tcall["VD"])
            else:
                tad = 0
            if tdp != 0:
                tvf = int(tad) / float(tdp)
            else:
                tvf = 0
            record.add_info("set", "VarDict")
            if (      (tmq >= int(self.minQual))
                    & (tdp >= int(self.totalDepth))
                    & (tad >= int(self.alleleDepth))
                    & (tvf >= float(self.variantFraction))
                ):
                    if complex_flag:
                        vcf_complex_writer.write_record(record)
                    else:
                        vcf_writer.write_record(record)
                    out_line = str.encode(
                        self.sampleName
                        + "\t"
                        + record.CHROM
                        + "\t"
                        + str(record.POS)
                        + "\t"
                        + str(record.REF)
                        + "\t"
                        + str(record.ALT[0])
                        + "\t"
                        + "."
                        + "\n"
                    )
                    txt_fh.write(out_line)

        vcf_writer.close()
        vcf_complex_writer.close()
        txt_fh.close()
        return self.vcf_out, self.vcf_complex_out, self.txt_out

    def filter_case_control(self):
        # TODO: continue to simplify method since we are now only worried about tumor/control vcf 
        '''
        @Description : The purpose of this function is to filter VCFs output from vardict that contain control sample info 
        @Created : 04/20/2022
        @author : Karthigayini Sivaprakasam, Eric Buehler 
        -input: self 
        -ouput: 
            - self.vcf_out
            - self.vcf_complex_out
            - self.txt_out
        '''
        if_swap_sample = False
        # If the caller reported the normal genotype column before the tumor, swap those around
        if self.allsamples[1] == self.sampleName:
            if_swap_sample = True
            self.vcf_reader.samples[0] = self.allsamples[1]
            self.vcf_reader.samples[1] = self.allsamples[0]

        normal_sampleName = self.vcf_reader.samples[1]

        vcf_writer = vcf.Writer(open(self.vcf_out, "w"), self.vcf_reader)
        vcf_complex_writer = vcf.Writer(open(self.vcf_complex_out, "w"), self.vcf_reader)
        txt_fh = open(self.txt_out, "wb")

        # mutations 

        # Iterate through rows and filter mutations
        for record in self.vcf_reader:
            tcall = record.genotype(self.sampleName)

            # Pad complex indels for proper genotyping
            if (
                record.INFO["TYPE"] == "Complex"
                and len(record.REF) != len(record.ALT)
                and record.INFO["SHIFT3"] > 0
                and record.INFO["SHIFT3"] <= len(record.INFO["LSEQ"])
            ):
                padding_seq = record.INFO["LSEQ"][
                    len(record.INFO["LSEQ"]) - (record.INFO["SHIFT3"] + 1) :
                ]
                record.REF = padding_seq + record.REF
                for alt in record.ALT:
                    alt.sequence = padding_seq + alt.sequence
                record.POS = record.POS - (record.INFO["SHIFT3"] + 1)
                record.INFO["SHIFT3_ADJUSTED"] = record.INFO["SHIFT3"]
                record.INFO["SHIFT3"] = 0
                complex_flag = True
            else:
                complex_flag = False
                record.INFO["SHIFT3_ADJUSTED"] = 0

            keep_based_on_status = True
            try:
                if "Somatic" not in record.INFO["STATUS"] and self.filterGermline:
                    keep_based_on_status = False
            except KeyError:
                keep_based_on_status = False
            try:
                if tcall["QUAL"] is not None:
                    tmq = int(tcall["QUAL"])
                else:
                    tmq = 0
            except:
                tmq = int(record.INFO["QUAL"])
          
            if tcall["DP"] is not None:
                tdp = int(tcall["DP"][0])
            else:
                tdp = 0
            if tcall["VD"] is not None:
                tad = int(tcall["VD"])
            else:
                tad = 0
            if tdp != 0:
                tvf = int(tad) / float(tdp)
            else:
                tvf = 0
            #### processing normal sample 
            # Read record for normal sample
            ncall = record.genotype(normal_sampleName)
            if ncall:
                if ncall["QUAL"] is not None:
                    nmq = int(ncall["QUAL"])
                else:
                    nmq = 0
                if ncall["DP"] is not None:
                    ndp = int(ncall["DP"][0])
                else:
                    ndp = 0
                if ncall["VD"] is not None:
                    nad = int(ncall["VD"])
                else:
                    nad = 0
                if ndp != 0:
                    nvf = nad / ndp
                else:
                    nvf = 0
                nvfRF = int(self.tnRatio) * nvf

            record.add_info("set", "VarDict")
            if_swap_sample=False
            if self.allsamples[1] == self.sampleName:
                if_swap_sample = True
                self.vcf_reader.samples[0] = self.allsamples[1]
                self.vcf_reader.samples[1] = self.allsamples[0]
            normal_sampleName = self.vcf_reader.samples[1]
            '''
                if if_swap_sample:
                nrm = record.samples[0]
                tum = record.samples[1]
                record.samples[0] = tum
                record.samples[1] = nrm
            '''
            if tvf > nvfRF: 
                if (
                    keep_based_on_status
                    & (tmq >= int(self.minQual))
                    & (nmq >= int(self.minQual))
                    & (tdp >= int(self.totalDepth))
                    & (tad >= int(self.alleleDepth))
                    & (tvf >= float(self.variantFraction))
                ):
                    if complex_flag:
                        vcf_complex_writer.write_record(record)
                    else:
                        vcf_writer.write_record(record)
                    out_line = str.encode(
                        self.sampleName
                        + "\t"
                        + record.CHROM
                        + "\t"
                        + str(record.POS)
                        + "\t"
                        + str(record.REF)
                        + "\t"
                        + str(record.ALT[0])
                        + "\t"
                        + "."
                        + "\n"
                    )
                    txt_fh.write(out_line)

        vcf_writer.close()
        vcf_complex_writer.close()
        txt_fh.close()
        return self.vcf_out, self.vcf_complex_out, self.txt_out
