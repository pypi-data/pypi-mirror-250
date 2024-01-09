#!/usr/bin/env python
# imports 
from __future__ import division
import os
import sys
import vcf
import time
import logging
from pathlib import Path
from typing import List, Optional
import typer
from vcf.parser import _Info as VcfInfo, _Format as VcfFormat, _vcf_metadata_parser as VcfMetadataParser
from .annotate_class import maf_annotater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

logger = logging.getLogger("filter")

app = typer.Typer(help="annotations for genomic files based on some criteria in a reference file")
# single filter 
# maf_maf = typer.Typer()
# app.add_typer(maf_maf, name="maf_maf", help="annotate a maf based on another maf")

@app.command("maf_maf")
def maf_maf(
    input_maf: Path = typer.Option(
        ...,
        "--input_maf",
        "-m",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input maf file which needs to be tagged",
    ),
    reference_maf: Path = typer.Option(
        ...,
        "--reference_maf",
        "-h",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input maf file which has hotspots",
    ),
    output_maf: str = typer.Option(
        'output_maf',
        "--output_maf",
        help="Output maf file name",
    )
):

    '''
    This tool helps to filter vardict version 1.4.6 VCFs for single sample calling
    '''
    logger.info("process_vardict: Started the run for doing standard filter.")
    annotated = maf_annotater(input_maf, reference_maf, output_maf).tag_hotspots()
    return 1

if __name__ == "__main__":
    app()
