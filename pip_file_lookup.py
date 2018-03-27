#! /usr/bin/env python3

import os
import sys
import pip.utils

if __name__ == '__main__':
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
            sys.stderr.write('Cannot get files for pkg: {}'.format(dist.project_name))

        if sys.argv[1] in paths_absolute:
            print(dist.project_name)
