# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

from pathlib import Path


_pkg_root = Path(__file__).parent.absolute()


# ==========================================================================================
# Do not change
# ==========================================================================================

__version__ = '0.1.6'

# These are the xsuite modules that are used by boinc and the versions they are tied to.
# This will be automatically updated from the active environment when making a minor release.
# If a new package needs to be pinned, add it here with a random version number,
# and similarily in the pyproject.toml
__xsuite__versions__ = {
    'xobjects' : '0.2.10',
    'xdeps'    : '0.5.2',
    'xpart'    : '0.16.3',
    'xtrack'   : '0.48.1',
    'xfields'  : '0.15.0',
    'xcoll'    : '0.2.7',
}

# ==========================================================================================
