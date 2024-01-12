from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from typing import Iterable, List, Union

import pandas as pd
from bioservices import BioDBNet
from tqdm import tqdm

from multi_bioservices.input_database import InputDatabase
from multi_bioservices.output_database import OutputDatabase
from multi_bioservices.taxon_id import TaxonID
from multi_bioservices.utils import get_biodbnet

_DEFAULT_OUTPUT_DB: Iterable[OutputDatabase] = (
    OutputDatabase.GENE_SYMBOL,
    OutputDatabase.GENE_ID,
    OutputDatabase.CHROMOSOMAL_LOCATION
)


def db2db(
    input_values: Union[List[str], List[int]],
    input_db: InputDatabase,
    output_db: Union[OutputDatabase, Iterable[OutputDatabase]] = _DEFAULT_OUTPUT_DB,
    taxon_id: Union[TaxonID, int] = TaxonID.HOMO_SAPIENS,
    remove_duplicates: bool = False,
    max_threads: int = 5,
    chunk_size: int = 300,
    cache: bool = True,
    verbose: bool = False,
    progress_bar: bool = False,
    tqdm_kwargs: dict = None
) -> pd.DataFrame:
    input_values: List[str] = list(map(str, input_values))
    taxon_id_value: int = int(taxon_id.value) if isinstance(taxon_id, TaxonID) else int(taxon_id)
    input_db_value: str = input_db.value
    output_db_values: List[str] = [output_db.value] if isinstance(output_db, OutputDatabase) \
        else [str(i.value) for i in output_db]
    
    # Check if input_db_value is in output_db_values
    if input_db_value in output_db_values:
        raise ValueError("Input database cannot be in output database")
    
    # Validate input settings
    max_threads = min(max_threads, 20)
    if chunk_size > 500 and taxon_id_value == TaxonID.HOMO_SAPIENS.value:
        print(f"Batch length greater than the maximum value of 500 for Homo Sapiens."
              f"Automatically setting batch length to 500")
        chunk_size = 500
    elif chunk_size > 300:
        print(f"Batch length greater than the maximum allowed value for Taxon ID of {taxon_id_value}."
              f"Automatically setting batch length to 300")
        chunk_size = 300
    
    # Perform conversion using BioDBNet's db2db
    conversion_df: pd.DataFrame = pd.DataFrame()
    biodbnet: BioDBNet = get_biodbnet(verbose=verbose, cache=cache)
    partial_func = partial(biodbnet.db2db, input_db=input_db_value, output_db=output_db_values, taxon=taxon_id_value)
    if progress_bar:
        tqdm_kwargs = tqdm_kwargs or {}
        total = tqdm_kwargs.pop("total", len(input_values))
        pbar = tqdm(total=total, **tqdm_kwargs)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(partial_func, input_values=input_values[i:i + chunk_size])
            for i in range(0, len(input_values), chunk_size)
        ]
        
        for future in as_completed(futures):
            if progress_bar:
                pbar.update(chunk_size)
            
            conversion_df = pd.concat([
                conversion_df,
                future.result()
            ])
    
    conversion_df = conversion_df.reset_index(names=[input_db_value])
    
    if remove_duplicates:
        # Remove rows that have duplicates in the input_db_value
        conversion_df = conversion_df.drop_duplicates(subset=[input_db_value])
    return conversion_df


if __name__ == "__main__":
    df = db2db(
        input_values=[str(i) for i in range(100)],
        input_db=InputDatabase.GENE_ID,
        output_db=OutputDatabase.ENSEMBL_GENE_ID,
        taxon_id=TaxonID.HOMO_SAPIENS,
        chunk_size=25,
        progress_bar=True,
    )
    print(df)
