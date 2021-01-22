import globals as g
from os import walk
from os.path import join

def get_files(path):    
    g.logger.info(f'Getting files for path {path}')
    _, _, files = next(walk(path))
    return files

def get_canonical_path(path):
    g.logger.info(f'Getting canonical path for path {path}')
    return join(g.base_dir, path)