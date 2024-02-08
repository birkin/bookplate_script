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

def read_marc_file( marc_file_path: pathlib.Path ) -> list:
    """ Reads the marc file and returns the data. 
        Called by manager.run_report() """
    log.debug( f'reading marc file ``{marc_file_path}``' )
    with open( marc_file_path, 'r') as fh:
        pymarc_records = pymarc.marcxml.parse_xml_to_array( fh )
    log.debug( f'number of records in file, ``{len(pymarc_records)}``' )
    return pymarc_records


def process_pymarc_record( pymarc_record: pymarc.record.Record ) -> dict:
    """ Processes the record and returns bookplate-data, if any. 
        Called by manager.run_report() """
    bookplate_data = {}
    bookplate_996_u_info: str = parse_996_u( pymarc_record );
    if bookplate_996_u_info:
        log.debug( 'bookplate data found' )
        bookplate_996_z_info = parse_996_z( pymarc_record )
        mms_id: str = parse_mms_id( pymarc_record )
        title = pymarc_record.title
        bookplate_data = { 
            'bookplate_996_u_info': bookplate_996_u_info,
            'bookplate_996_z_info': bookplate_996_z_info,
            'mms_id': mms_id,
            'title': title 
            }
    else:
        log.debug( 'no bookplate data found' )
    log.debug( f'bookplate_data, ``{pprint.pformat(bookplate_data)}``' )
    return bookplate_data


def parse_996_u( pymarc_record: pymarc.record.Record ) -> str:
    """ Parses the 996 field and returns the u-value, if any. 
        Called by process_pymarc_record() """
    field_996_u = ''
    try:
        field_996 = pymarc_record.get_fields('996')[0]
        field_996_u = field_996.get_subfields('u')[0]
    except:
        pass
    log.debug( f'field_996_u, ``{field_996_u}``' )
    return field_996_u


def parse_996_z( pymarc_record: pymarc.record.Record ) -> str:
    """ Parses the 996 field and returns the z-value, if any. 
        Called by process_pymarc_record() """
    field_996_z = ''
    try:
        field_996 = pymarc_record.get_fields('996')[0]
        field_996_z = field_996.get_subfields('z')[0]
    except:
        pass
    log.debug( f'field_996_z, ``{field_996_z}``' )
    return field_996_z


def parse_mms_id( pymarc_record: pymarc.record.Record ) -> str:
    """ Parses the 001 field and returns the mms_id. 
        Called by process_pymarc_record() """
    mms_id = pymarc_record['001'].data
    log.debug( f'mms_id, ``{mms_id}``' )
    return mms_id