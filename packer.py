from rjsmin import jsmin
import json
import argparse
import globals as g
from shutil import copy
from logger import Logger
from utils import get_files, get_canonical_path
from os import getcwd, walk, sep, makedirs
from os.path import basename, join, expandvars, expanduser, isfile, isdir, relpath

file_list = []

includes = []
excludes = []
entryPoints = []

g.base_dir = getcwd()

def start_pack():
    #TODO Do more minification
    makedirs('dist', exist_ok=True)
    for f in includes:
        f = relpath(f, g.base_dir)
        g.logger.debug(f)
        if f.startswith('..'):
            print(f'Excluding: {f} : falls outside of the pack directory, path structure can\'t be preserved.')
            continue
        if f.endswith('.js'):
            with open(f'dist/{f}', 'w+') as output_file:
                with open(f'{f}', 'r') as in_file:
                    output_file.writelines(jsmin(in_file.read()))
        elif f.endswith('.json'):
            with open(f'dist/{f}', 'w+') as output_file:
                with open(f'{f}', 'r') as in_file:
                    output_file.writelines(json.dumps(json.load(in_file), separators=(',', ':')))
        else:
            g.logger.info(f'Making if not exists: dist/{f[0:f.rindex("/")]}')
            makedirs(f'dist/{f[0:f.rindex("/")]}', exist_ok=True)
            g.logger.info(f'Copying {f} to /dist/{f}')
            copy(f, f'dist/{f}')




def init_cmd():
    files = get_files(g.base_dir)
    if 'pack.json' in files:
        print('pack.json already present, aborting...')
    else:
        g.logger.info('Creating pack.json')
        with open('pack.json', 'x') as pack_file:
            pack_file.writelines(json.dumps(
                {'includes': [], 'excludes': [], 'entryPoints': []}, indent=4))


def pack_cmd():
    files = get_files(g.base_dir)
    if 'pack.json' in files:
        with open(join(g.base_dir, 'pack.json')) as configFile:
            config = json.load(configFile)
            g.logger.debug(config)
            entryPoints = config['entryPoints']
            build_black_list(config['excludes'])
            g.logger.debug(f'BL: {excludes}')
            build_white_list(config['includes'])
            g.logger.debug(f'WL: {includes}')
            #TODO Make entrypoints work

            start_pack()
    else:
        print('No pack.json in this directory, exiting...')


def print_expanded_help():
    print('USAGE:')


def build_black_list(paths):
    for path in paths:
        path = expanduser(expandvars(path))
        if not path.startswith('/'):
            path = get_canonical_path(path)
        if isfile(path):
            excludes.append(path)
        else:
            for root, dirs, files in walk(path):
                for f in files:
                    f = join(root, f)
                next_list = []
                for d in dirs:
                    d = join(root, d)
                    next_list.append(d)
                build_black_list(next_list)


def build_white_list(paths):
    g.logger.info(f'Building whitelist from paths {paths}')
    for path in paths:
        path = expanduser(expandvars(path))
        if not path.startswith('/'):
            path = get_canonical_path(path)
        if isfile(path):
            includes.append(path)
        else:
            for root, _, files in walk(path):
                g.logger.debug(f'{root} | {files}')
                for f in files:
                    f = join(root, f)
                    if f not in excludes:
                        includes.append(f)


def main():
    parser = argparse.ArgumentParser(
        description='Packs a web extension for distribution')
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increment verbosity')
    subparser = parser.add_subparsers(title='commands')
    pack_parser = subparser.add_parser('pack', help='pack the extension')
    pack_parser.set_defaults(func=pack_cmd)
    init_parser = subparser.add_parser('init', help='initialize a pack.json')
    init_parser.set_defaults(func=init_cmd)
    help_parser = subparser.add_parser('help', help='extended help and usage')
    help_parser.set_defaults(func=print_expanded_help)
    args = parser.parse_args()
    g.logger = Logger(args.verbose)
    g.logger.debug(args)
    try:
        args.func()
    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()
