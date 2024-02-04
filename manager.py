## stdlib
import argparse, logging, os, pathlib
from pathlib import Path

## 3rd party
from dotenv import load_dotenv, find_dotenv

## local
from lib.helpers import decompress_file


## load envars ------------------------------------------------------
load_dotenv( find_dotenv(raise_error_if_not_found=True) )
LOG_LEVEL = os.environ['LOG_LEVEL']
MARC_DAILY_DIR_SOURCE = Path( os.environ['MARC_DAILY_DIR_SOURCE'] )
MARC_DAILY_DIR_OUTPUT = Path( os.environ['MARC_DAILY_DIR_OUTPUT'] )
MARC_FULL_DIR_SOURCE = Path( os.environ['MARC_FULL_DIR_SOURCE'] )
MARC_FULL_DIR_OUTPUT = Path( os.environ['MARC_FULL_DIR_OUTPUT'] )


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
    compressed_marc_files = [ f for f in MARC_FULL_DIR_SOURCE.glob('*.tar.gz') ]  # creates list of pathlib objects
    log.debug( f'found ``{len(compressed_marc_files)}`` marc files in ``{MARC_FULL_DIR_SOURCE}``' )

    for compressed_f_pathobj in compressed_marc_files:
        log.debug( f'processing ``{compressed_f_pathobj}``' )
        ## extract the .tar.gz files --------------------------------
        decompress_file( compressed_f_pathobj, "foo" )
        ## process the .mrc file ------------------------------------
        pass
        break  # temp, for development

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
    