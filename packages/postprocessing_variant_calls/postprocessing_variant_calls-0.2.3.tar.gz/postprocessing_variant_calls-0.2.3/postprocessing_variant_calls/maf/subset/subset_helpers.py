from pathlib import Path
from typing import List, Optional
import typer
import pandas as pd

app = typer.Typer()
#TODO need to make this accessible from all locations
def read_tsv(tsv, separator):
    """Read a tsv file

    Args:
        maf (File): Input MAF/tsv like format file

    Returns:
        data_frame: Output a data frame containing the MAF/tsv
    """
    typer.echo("Read Delimited file...")
    skip = get_row(tsv)
    return pd.read_csv(tsv, sep=separator, skiprows=skip, low_memory=False)


def read_ids(sid, ids):
    """make a list of ids

    Args:
        sid (tuple): Multiple ids as tuple
        ids (File): File containing multiple ids

    Returns:
        list: List containing all ids
    """
    typer.echo("Make a list of IDs...")
    if not sid:
        with open(ids) as file:
            sid = file.read().splitlines()[1:]
    return sid


def filter_by_columns(sid, tsv_df):
    """Filter data by columns

    Args:
        sid (list): list of columns to subset over
        tsv_df (data_frame): data_frame to subset from

    Returns:
        data_frame: A copy of the subset of the data_frame
    """
    typer.echo("Subset based on columns...")
    subset_tsv = tsv_df.filter(items=sid)
    return subset_tsv.copy(deep=True)


def filter_by_rows(sid, tsv_df, col_name):
    """Filter the data by rows

    Args:
        sid (list): list of row names to subset over
        tsv_df (data_frame): data_frame to subset from
        col_name (string): name of the column to filter using names in the sid

    Returns:
        data_frame: A copy of the subset of the data_frame
    """
    typer.echo("Subset based on rows...")
    ns = set(sid)
    pattern = "|".join([r"\b{}\b".format(i) for i in ns])
    result = tsv_df[tsv_df[col_name].str.contains(pattern, regex=True, na=False)]
    if result.empty: 
        typer.echo("no rows containing the specified ids of: {ids}".format(ids=ns))
    return result.copy(deep=True)
# preprocessing
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
def check_separator(separator: str):
    separator_dict = {"tsv":'\t', "csv":","}
    if separator in separator_dict.keys():
        sep = separator_dict[separator]
    else:
        typer.secho(f"Separator for delimited file must be 'tsv' or 'csv', not '{separator}'", fg=typer.colors.RED)
        raise typer.Abort()
    return sep

if __name__ == "__main__":
    app()
