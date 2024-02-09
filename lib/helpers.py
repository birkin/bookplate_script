import json, logging, pathlib, os, pprint, re, tarfile
from pathlib import Path

import pymarc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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


def check_bruknow( bookplate_data: dict ) -> dict:
    """ Checks BruKnow via Selenium to see if the bookplate exists, and updates bookplate_data with result.
        Called by manager.run_report() """
    if bookplate_data:
        url_pattern = 'https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma{MMS_ID_HERE}&context=L&vid=01BU_INST:BROWN&lang=en'
        url = url_pattern.format( MMS_ID_HERE=bookplate_data['mms_id'] )
        log.debug( f'url, ``{url}``' )
        driver = webdriver.Firefox()
        try:
            driver.get( url )
            WebDriverWait( driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Bookplate\')]")))
            elements = driver.find_elements(By.XPATH, "//span[contains(.,\'Bookplate\')]")
            assert len(elements) > 0
            elements = driver.find_elements(By.CSS_SELECTOR, "div > prm-highlight .bul_pl_primo_bookplate_image")
            assert len(elements) > 0
            elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "Purchased")
            assert len(elements) > 0
            msg = f'bookplate found at, ``{url}``'
        except Exception as e:
            msg = f'problem with BruKnow check, ``{e}``'
            log.exception( msg )
        finally:
            driver.quit()
        bookplate_data['bruknow_check'] = msg
    else:
        log.debug( 'no bookplate data to check' )
    return bookplate_data






def save_bookplate_json( bookplate_data: dict, output_dir: pathlib.Path ) -> None:
    """ Saves the bookplate data as a json file. 
        Called by manager.run_report() """
    if bookplate_data:
        data_to_save = bookplate_data
        mms_id = bookplate_data['mms_id']
        output_filepath: pathlib.Path = output_dir / f'{mms_id}.json'
        log.debug( f'output_filepath, ``{output_filepath}``' )
        ## handle existing data -------------------------------------
        if output_filepath.exists():
            log.warning( f'existing data found for mms_id, ``{mms_id}``' )
            with open( output_filepath, 'r' ) as f:
                existing_data = json.load( f )
                ## if existing_data is a dict, add that dict to a list, then append the new data
                if type( existing_data ) == dict:
                    existing_data = [ existing_data ]
                    existing_data.append( bookplate_data )
                ## if existing_data is a list, append the new data
                elif type( existing_data ) == list:
                    existing_data.append( bookplate_data )
                    data_to_save = existing_data
                else:
                    msg = f'uh-oh -- existing_data is not a dict or a list, ``{existing_data}``'
                    log.exception( msg )
                    raise Exception( msg )
        else:
            ## handle new data --------------------------------------
            log.debug( 'new data' )
        # jsn = json.dumps( data_to_save, sort_keys=True )
        jsn = json.dumps( data_to_save, sort_keys=True, indent=2 )
        with open( output_filepath, 'w' ) as f:
            f.write( jsn )
    return
