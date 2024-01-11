# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import json
import tarfile
from pathlib import Path
import tempfile
import numpy as np

import xobjects as xo

from .user import get_domain, get_directory
from .server import fs_mv, missing_eos, timestamp
from .simulation_io import SimConfig, app_version, assert_versions


def _get_num_elements_from_line(line):
    if line is None:
        return {}
    elements = np.unique([ee.__class__.__name__ for ee in line.elements],
                         return_counts=True)
    return dict(zip(*elements))


class SubmitJobs:

    def __init__(self, user, study_name, line=None, dev_server=False):
        assert_versions()
        if not dev_server:
            raise NotImplementedError("Regular server not yet operational. "
                                    + "Please use dev_server=True.")
        if '__' in study_name:
            raise ValueError("The character sequence '__' is not allowed in 'study_name'!")
        self._user = user
        self._domain = get_domain(user)
        if self._domain=='eos':
            missing_eos()
        if dev_server:
            self._target = get_directory(user) / 'input_dev'
        else:
            self._target = get_directory(user) / 'input'
        self._study_name = study_name
        self._line = line
        self._num_elements = _get_num_elements_from_line(line)
        self._submit_file = f"{self._study_name}__{timestamp()}.tar.gz"
        self._json_files = []
        self._bin_files = []
        self._temp    = tempfile.TemporaryDirectory()
        self._tempdir = Path(self._temp.name).resolve()
        self._tempdir.mkdir(parents=True, exist_ok=True)
        self._submitted = False


    def _assert_not_submitted(self):
        if self._submitted:
            raise ValueError("Jobs already submitted! Make a new SubmitJobs object to continue.")


    def add(self, *, job_name, num_turns, particles, line=None, checkpoint_every=-1, **kwargs):
        self._assert_not_submitted()
        if '__' in job_name:
            raise ValueError("The character sequence '__' is not allowed in 'job_name'!")
        if line is None:
            if self._line is None:
                raise ValueError("Need to provide a line! This can be done for "
                               + "each job separately, or at the SubmitJobs init.")
            line = self._line
            num_elements = self._num_elements
        else:
            num_elements = _get_num_elements_from_line(line)
        filename = f"{self._user}__{timestamp(ms=True)}"
        json_file = Path(self._tempdir, f"{filename}.json")
        bin_file  = Path(self._tempdir, f"{filename}.bin")
        # TODO: warn if job expected to be too short ( < 90s)
        json_dict = {
            'user': self._user,
            'study_name': self._study_name,
            'job_name': job_name,
            'xboinc_ver': app_version,
            'num_elements': num_elements,
            'num_part': len(particles.state[particles.state > 0]),
            'num_turns': num_turns,
            **kwargs
        }
        with json_file.open('w') as fid:
            json.dump(json_dict, fid, cls=xo.JEncoder)
        SimConfig.build(filename=bin_file, num_turns=num_turns, line=line,
                         particles=particles, checkpoint_every=checkpoint_every)
        self._json_files += [json_file]
        self._bin_files  += [bin_file]


    def submit(self):
        self._assert_not_submitted()
        with tarfile.open(self._tempdir / self._submit_file, "w:gz") as tar:
            for thisfile in self._json_files + self._bin_files:
                tar.add(thisfile, arcname=thisfile.name)
        if self._domain == 'eos' or self._domain == 'afs':
            fs_mv(self._tempdir / self._submit_file, self._target)
        else:
            raise ValueError(f"Wrong domain {self._domain} for user {self._user}!")
        self._submitted = True
        # TODO: check that tar contains all files
        # clean up
        for thisfile in self._json_files + self._bin_files:
            thisfile.unlink()
        self._temp.cleanup()

