# -*- coding: utf-8 -*-
VERSION = (0, 3, 2, 'final', 0)


def get_version():
    """Get app version."""
    version = "{0}.{1}".format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "{0}.{1}".format(version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = "{0} pre-alpha".format(version)
    else:
        if VERSION[3] != 'final':
            version = "{0} {1} {2}".format(version, VERSION[3], VERSION[4])
    return version
