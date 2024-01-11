# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import sys
import numpy as np
from pathlib import Path

import xobjects as xo
import xpart as xp
import xtrack as xt

from .version import assert_versions
from .default_tracker import get_default_tracker
from .output import SimState


# The build time of the input file is largely dominated by the rebuilding of the
# tracker. For this reason we cache the line, such that when submitting many jobs
# on the same line only the first job creation takes some time.
#
# Note that this advantage is lost when changing lines at every job, in other
# words, one should be smart in organising the order of jobs to have a speedy
# submission.
_previous_line_cache = {}


class ElementRefData(xo.Struct):
    # Stub; this is defined inside Tracker
    pass


class SimConfig(xo.Struct):
    line_metadata    = xo.Ref(ElementRefData)
    num_turns        = xo.Int64
    num_elements     = xo.Int64
    checkpoint_every = xo.Int64
    sim_state        = xo.Ref(SimState)

    def __init__(self, *args, **kwargs):
        assert_versions()
        if '_xobject' not in kwargs:
            default_tracker, default_config_hash = get_default_tracker()
            tracker_data = default_tracker._tracker_data_cache[default_config_hash]
            kwargs['line_metadata'] = xo.Ref(tracker_data._element_ref_data.__class__)
        super().__init__(**kwargs)


    @classmethod
    def build(cls, *, num_turns, line, particles, checkpoint_every=-1, filename=None):

        # Default tracker (cached, only compiles the first time)
        default_tracker, default_config_hash = get_default_tracker()

        # Assemble data structure
        simbuf = xo.ContextCpu().new_buffer()
        sim_config = cls(_buffer=simbuf)

        # Check line compatibility and tracker (also cached)
        if 'line' not in _previous_line_cache\
        or _previous_line_cache['line'] != line:
            _check_compatible_elements(line, default_tracker)
            line.discard_tracker()
            line.build_tracker(_context=simbuf.context, _buffer=simbuf,
                                track_kernel=default_tracker.track_kernel)
            if default_config_hash not in line.tracker._tracker_data_cache:
                raise RuntimeError('Tracker data for default config not found')
            _previous_line_cache['line'] = line

        # Create SimConfig metadata
        tracker_data = line.tracker._tracker_data_cache[default_config_hash]
        sim_config.line_metadata = tracker_data._element_ref_data
        sim_config.num_turns = num_turns
        sim_config.num_elements = len(line.element_names)
        sim_config.checkpoint_every = checkpoint_every
        sim_state = SimState(particles=particles, i_turn=0, _buffer=simbuf)
        sim_config.sim_state = sim_state._xobject
        sim_state.size = sim_state._xobject._size # store size of sim_state TODO: in init of SimState
        assert sim_config._offset == 0
        assert sim_config._fields[0].offset == 0

        # Write sim buffer to file
        if filename is not None:
            filename = Path(filename).expanduser().resolve()
            with filename.open('wb') as fid:
                fid.write(simbuf.buffer.tobytes())

        return sim_config


def _check_compatible_elements(line, default_tracker):
    default_elements = [ee.__class__.__name__ for ee in default_tracker.line.elements]
    elements = np.unique([ee.__class__.__name__ for ee in line.elements])
    for ee in elements:
        if ee not in default_elements:
            raise ValueError(f"Element of type {ee} not supported "
                           + f"in this version of xboinc!")
    