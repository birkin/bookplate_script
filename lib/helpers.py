import logging, pathlib, os, pprint, re, tarfile
from pathlib import Path

import pymarc


log = logging.getLogger( __name__ )  # configured in manager.py


def sort_unpadded_filenames( unsorted_filenames: list ) -> list:
    """ Sorts a list of filenames that have unpadded numbers. 
        A simple sort would put 10 after 1, etc. 
        Called by manager.run_report() """
    log.debug( f'unsorted_filenames (first few), ``{pprint.pformat(unsorted_filenames[0:3])}``' )
    sorted_filenames = sorted( unsorted_filenames, key=unpadded_sort_key )    
    log.debug( f'sorted_filenames (first few), ``{pprint.pformat(sorted_filenames[0:3])}``' )
    return sorted_filenames


def unpadded_sort_key( path: pathlib.Path ) -> int:
    """ Extracts the number from the filename and returns it as an integer. 
        Note: path.stem still includes .tar, ie `Full_set_bibs_new_147.tar` -- but that doesn't matter for the regex
        Called by sort_unpadded_filenames()"""
    numbers = re.findall(r'\d+', path.stem)  # so for `Full_set_bibs_new_147.tar`, this captures [147]
    # log.debug( f'numbers, ``{numbers}``' )
    num: int = 0  # default case, but number should always be found
    if numbers:
        num = int(numbers[-1])
    return num


def decompress_file( source_path: pathlib.Path, output_path_dir: pathlib.Path ) -> Path:
    """ Decompresses the file and saves it to the destination-path. 
        Returns output_path.
        Called by manager.run_report() """
    log.debug( f'decompressing ``{source_path}`` to ``{output_path_dir}``' )
    ## extract and save file ----------------------------------------
    with tarfile.open( source_path, 'r:gz' ) as tar:  # 'r' for read; 'gz' for gzip decompression
        tar.extractall( path=output_path_dir )
    ## remove .tar.gz part of filename ------------------------------
    base_name = source_path.stem  # this removes the '.gz' part of 'foo.tar.gz' part
    log.debug( f'base_name 1, ``{base_name}``' )
    base_name = base_name.split( '.tar' )[0]  # This removes the '.tar' part
    log.debug( f'base_name 2, ``{base_name}``' )
    ## add .xml -----------------------------------------------------
    output_file_name = f'{base_name}.xml'
    log.debug( f'output_file_name, ``{output_file_name}``' )
    ## construct full output path -----------------------------------
    output_file_path = Path( output_path_dir / output_file_name )
    log.debug( f'output_path, ``{output_file_path}``' )
    ## update permissions --------------------------------------------
    os.chmod( output_file_path, 0o664 )  # `0o664`` is the octal representation of `rw-rw-r--``
    return output_file_path


def process_marc_file( marc_file_path: pathlib.Path ) -> dict:
    """ Processes the marc file and returns the data. 
        Called by manager.run_report() """
    log.debug( f'processing marc file ``{marc_file_path}``' )

    # pymarc_records = []
    with open( marc_file_path, 'r') as fh:
        pymarc_records: list = pymarc.marcxml.parse_xml_to_array( fh )
        log.info( f'number of records in file, ``{len(pymarc_records)}``' )

    for record in pymarc_records:
        ## see if the 
        title = record.title
        log.debug( f'title, ``{title}``' )
        
    bookplate_data = {}
    log.debug( f'bookplate_data, ``{pprint.pformat(bookplate_data)}``' )
    return bookplate_data