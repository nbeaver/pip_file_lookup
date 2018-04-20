#! /usr/bin/env python3

import os.path
import argparse
import logging
import sys


def packages_with_path(path):
    # TODO: why is this import so slow?
    import pip.utils
    for dist in pip.utils.get_installed_distributions():
        # RECORDs should be part of .dist-info metadatas
        if dist.has_metadata('RECORD'):
            logging.info('package {} has RECORD metadata'.format(dist.project_name))
            lines = dist.get_metadata_lines('RECORD')
            paths = [l.split(',')[0] for l in lines]
            logging.debug(paths)
            paths_absolute = [os.path.normpath(os.path.join(dist.location, p)) for p in paths]
            logging.debug(paths_absolute)
        # Otherwise use pip's log for .egg-info's
        elif dist.has_metadata('installed-files.txt'):
            logging.info('package {} has .egg-info metadata'.format(dist.project_name))
            paths = dist.get_metadata_lines('installed-files.txt')
            logging.debug(paths)
            paths_absolute = [os.path.normpath(os.path.join(dist.egg_info, p)) for p in paths]
            logging.debug(paths_absolute)
        else:
            logging.error('cannot get files for package: {}'.format(dist.project_name))
            paths = []
            paths_absolute = []

        if path in paths_absolute:
            yield dist


def existing_file(path):
    if not os.path.exists(path):
        logging.warn('path does not exist: {}'.format(path))
    elif not os.path.isfile(path):
        # Directories are not listed in pip metadata.
        logging.warn('not a file: {}'.format(path))
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Show name of pip package for a given path.'
    )
    parser.add_argument(
        'path',
        type=existing_file,
        help='absolute path to file in pip package'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    matched_path = False
    for dist in packages_with_path(args.path):
        print(dist.project_name)
        matched_path = True

    if not matched_path:
        logging.error('could not match path: {}'.format(args.path))
        sys.exit(1)
