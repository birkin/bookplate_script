## stdlib
import argparse, logging, os, pathlib, pprint, time
from pathlib import Path

## 3rd party
import pymarc
from dotenv import load_dotenv, find_dotenv

## local
from lib import helpers


## load envars ------------------------------------------------------
load_dotenv( find_dotenv(raise_error_if_not_found=True) )
LOG_LEVEL = os.environ['LOG_LEVEL']
MARC_DAILY_SOURCE_DIR = Path( os.environ['MARC_DAILY_SOURCE_DIR'] )
MARC_DAILY_OUTPUT_DIR = Path( os.environ['MARC_DAILY_OUTPUT_DIR'] )
MARC_FULL_SOURCE_DIR = Path( os.environ['MARC_FULL_SOURCE_DIR'] )
MARC_FULL_OUTPUT_DIR = Path( os.environ['MARC_FULL_OUTPUT_DIR'] )
TRACKER_OUTPUT_PATH = Path( os.environ['TRACKER_OUTPUT_PATH'] )


## setup logging ----------------------------------------------------
lglvldct = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO }
logging.basicConfig(
    level=lglvldct[LOG_LEVEL],  # assigns the level-object to the level-key loaded from the envar
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger( __name__ )
log.debug( 'logging working' )
 

def run_report():
    ## set up a tracker ---------------------------------------------
    tracker: dict = helpers.init_tracker()
    ## list the .tar.gz files ---------------------------------------
    # unsorted_compressed_marc_files = [ f for f in MARC_FULL_SOURCE_DIR.glob('*.tar.gz') ]  # creates list of pathlib objects
    unsorted_compressed_marc_files = [ f for f in MARC_FULL_SOURCE_DIR.glob('*new.tar.gz') ]  # creates list of pathlib objects
    compressed_marc_files = helpers.sort_unpadded_filenames( unsorted_compressed_marc_files )
    tracker['step_01']['count_targz_files'] = len(compressed_marc_files)
    tracker['step_01']['elapsed_time'] = time.time() - tracker['start_elapsed']
    log.info( f'found ``{len(compressed_marc_files)}`` marc files in ``{MARC_FULL_SOURCE_DIR}``' )
    # log.debug( f'compressed_marc_files, ``{pprint.pformat(compressed_marc_files)}``')

    ## loop through the .tar.gz files -------------------------------
    total_records_count = 0
    total_records_with_bookplate_data_count = 0
    extracted_bookplate_data = []
    for ( i, compressed_f_pathobj ) in enumerate( compressed_marc_files ):
        log.debug( f'processing file ``{compressed_f_pathobj}``')
        ## extract the .tar.gz files --------------------------------
        output_filepath: Path = helpers.decompress_file( compressed_f_pathobj, MARC_FULL_OUTPUT_DIR )
        ## read marc-xml file ---------------------------------------
        pymarc_records: list = helpers.read_marc_file( output_filepath )
        assert type( pymarc_records[0] ) == pymarc.record.Record, type( pymarc_records[0] )
        total_records_count += len( pymarc_records )
        ## process records ---------------------------
        for (i, rcrd ) in enumerate( pymarc_records ):
            pymarc_record: pymarc.record.Record = rcrd
            bookplate_data: dict = helpers.process_pymarc_record( pymarc_record )
            if bookplate_data:
                total_records_with_bookplate_data_count += 1
                extracted_bookplate_data.append( bookplate_data )

            # helpers.save_bookplate_json( bookplate_data, MARC_FULL_OUTPUT_DIR )
            # if i >= 3:  # for testing
            #     log.debug( 'breaking after 3 records for testing' )
            #     break
            log.debug( 'this is where the inner break was' )
            # helpers.save_tracker( tracker, TRACKER_OUTPUT_PATH )


        total_files = len(compressed_marc_files)
        if (i + 1) % 3 == 0 or i == total_files - 1:  # After every 10 files or the last file
            log.info(f'Processed {i + 1} of {total_files} files.')
        ## delete the marc_xml data-file ----------------------------
        output_filepath.unlink()

        # if i >= 4:  # for testing
        #     break  
        # i += 1

    ## update extract-bookplate-data tracker ------------------------
    tracker['step_02']['count_all_marc_records'] = total_records_count
    tracker['step_02']['count_records_with_bookplate_data'] = total_records_with_bookplate_data_count
    tracker['step_02']['extacted_bookplate_data'] = extracted_bookplate_data
    tracker['step_02']['elapsed_time'] = time.time() - tracker['start_elapsed']

    ## check for bruknow bookplates ---------------------------------
    ## TODO  # bookplate_data: dict = helpers.check_bruknow( bookplate_data )


    ## update tracker -----------------------------------------------
    total_elapsed_time = time.time() - tracker['start_elapsed']
    log.debug( f'total_elapsed_time, ``{total_elapsed_time}``' )
    tracker['elapsed_total_time'] = total_elapsed_time
    del tracker['start_elapsed']  # removes tracker['start_elapsed'] key
    helpers.save_tracker( tracker, TRACKER_OUTPUT_PATH )
    log.info( 'done' )
    return


def run_daily_db_update():
    # ...
    print('will update daily db')
    # ...
    return


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', action='store_true', help='run report script')
    parser.add_argument('--update', action='store_true', help='run update script')
    parser.add_argument('--both', action='store_true', help='run both report and update scripts')
    args = parser.parse_args()

    if not args.report and not args.update and not args.both:
        print( 'Please provide either the --update, --report, or --both argument.' )
        exit(1)

    if args.report:
        run_report()
    elif args.update:
        run_daily_db_update()
    elif args.both:
        run_report()
        run_daily_db_update()
    