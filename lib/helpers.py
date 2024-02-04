import pathlib, tarfile
from pathlib import Path


def decompress_file( source_path: pathlib.Path, destination_path ):
    print( f'decompressing ``{source_path}`` to ``{destination_path}``' )
    return