# Main Import
import typer
from .vardict import vardict_process
# from .maf import main
from .maf import main
from .maf.annotate import annotate_process
from .maf.concat import concat_process
import logging
import time
# setup logger
logger = logging.getLogger("filter")
app = typer.Typer()

# Vardict filter App 
app.add_typer(vardict_process.app, name="vardict", help="post-processing commands for VarDict version 1.4.6 VCFs.")

# Add Annote Maf 
app.add_typer(main.app, name="maf", help="operations for manipulating maf files based on a given input.")

# Main App
if __name__ == "__main__":
    app()
