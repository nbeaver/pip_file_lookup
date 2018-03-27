#! /usr/bin/env python3

import os
import pip._vendor
import pip._vendor.packaging.utils
import sys

if __name__ == '__main__':

    for dist in pip._vendor.pkg_resources.working_set:
        name = pip._vendor.packaging.utils.canonicalize_name(dist.project_name)

        if isinstance(dist, pip._vendor.pkg_resources.DistInfoDistribution):
            # RECORDs should be part of .dist-info metadatas
            if dist.has_metadata('RECORD'):
                lines = dist.get_metadata_lines('RECORD')
                paths = [l.split(',')[0] for l in lines]
                paths_absolute = [os.path.join(dist.location, p) for p in paths]
        else:
            # Otherwise use pip's log for .egg-info's
            if dist.has_metadata('installed-files.txt'):
                paths = dist.get_metadata_lines('installed-files.txt')
                paths_absolute = [os.path.join(dist.egg_info, p) for p in paths]

        if sys.argv[1] in paths_absolute:
            print(name)
