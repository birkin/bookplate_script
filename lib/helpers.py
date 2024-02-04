import logging, pathlib, pprint, re, tarfile
from pathlib import Path


log = logging.getLogger( __name__ )  # configured in manager.py


def sort_unpadded_filenames( unsorted_filenames: list ) -> list:
    """ Sorts a list of filenames that are unpadded numbers. 
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


def make_output_path( compressed_f_pathobj: pathlib.Path, output_dir: pathlib.Path ) -> pathlib.Path:
    """ Returns the output path for the decompressed file. 
        Called by manager.run_report() """
    log.debug( f'compressed_f_pathobj, ``{compressed_f_pathobj}``' )
    log.debug( f'output_dir, ``{output_dir}``' )
    tar_stem: str = compressed_f_pathobj.stem  # drops the .gz but still has the .tar (i know I could these `str`s in Path() but am leaving explicit for now)
    tar_stem_pathobj = Path( tar_stem )
    real_stem: str = tar_stem_pathobj.stem  # drops the .tar
    real_stem_pathobj = Path( real_stem )
    output_path = output_dir / real_stem_pathobj.with_suffix('.xml')
    log.debug( f'output_path, ``{output_path}``' )
    return output_path


def decompress_file( source_path: pathlib.Path, destination_path_dir: pathlib.Path ):
    """ Decompresses the file. 
        Called by manager.run_report() """
    log.debug( f'decompressing ``{source_path}`` to ``{destination_path_dir}``' )
    with tarfile.open( source_path, 'r:gz' ) as tar:  # 'r' for read; 'gz' for gzip decompression
        tar.extractall( path=destination_path_dir )
    return