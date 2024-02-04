import logging, pathlib, tarfile
from pathlib import Path


log = logging.getLogger( __name__ )


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