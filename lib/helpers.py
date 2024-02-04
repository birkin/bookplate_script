import logging, pathlib, tarfile
from pathlib import Path


log = logging.getLogger( __name__ )


def decompress_file( source_path: pathlib.Path, destination_path_dir: pathlib.Path ):
    log.debug( f'decompressing ``{source_path}`` to ``{destination_path_dir}``' )
    with tarfile.open( source_path, 'r:gz' ) as tar:  # 'r' for read; 'gz' for gzip decompression
        tar.extractall( path=destination_path_dir )

    return