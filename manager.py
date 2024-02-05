## stdlib
import argparse, logging, os, pathlib, pprint
from pathlib import Path

## 3rd party
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
    ## list the .tar.gz files ---------------------------------------
    unsorted_compressed_marc_files = [ f for f in MARC_FULL_SOURCE_DIR.glob('*.tar.gz') ]  # creates list of pathlib objects
    compressed_marc_files = helpers.sort_unpadded_filenames( unsorted_compressed_marc_files )
    log.info( f'found ``{len(compressed_marc_files)}`` marc files in ``{MARC_FULL_SOURCE_DIR}``' )
    # log.debug( f'compressed_marc_files, ``{pprint.pformat(compressed_marc_files)}``')

    for ( i, compressed_f_pathobj ) in enumerate( compressed_marc_files ):
        log.info( f'processing file ``{compressed_f_pathobj}``')
        ## extract the .tar.gz files --------------------------------
        helpers.decompress_file( compressed_f_pathobj, MARC_FULL_OUTPUT_DIR )
        ## process the .mrc file ------------------------------------
        pass
        if i >= 2:  # for testing
            break  
        i += 1

    # ...
    print('will generate report')
    # ...
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
    