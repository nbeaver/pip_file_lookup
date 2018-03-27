#! /usr/bin/env python3

import os
import argparse
import logging
import sys

def existing_path(path):
    if not os.path.exists(path):
        logging.warn('path does not exist: {}'.format(path))
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Show name of pip package for a given path.'
    )
    parser.add_argument(
        'path',
        type=existing_path,
        help='path to file or directory in pip package'
    )
    args = parser.parse_args()

    import pip.utils
    matched_path = False
    for dist in pip.utils.get_installed_distributions():
        # RECORDs should be part of .dist-info metadatas
        if dist.has_metadata('RECORD'):
            lines = dist.get_metadata_lines('RECORD')
            paths = [l.split(',')[0] for l in lines]
            paths_absolute = [os.path.join(dist.location, p) for p in paths]
        # Otherwise use pip's log for .egg-info's
        elif dist.has_metadata('installed-files.txt'):
            paths = dist.get_metadata_lines('installed-files.txt')
            paths_absolute = [os.path.join(dist.egg_info, p) for p in paths]
        else:
            logging.error('cannot get files for pkg: {}'.format(dist.project_name))

        if args.path in paths_absolute:
            matched_path = True
            print(dist.project_name)

    if not matched_path:
        logging.error('could not match path: {}'.format(args.path))
        sys.exit(1)
