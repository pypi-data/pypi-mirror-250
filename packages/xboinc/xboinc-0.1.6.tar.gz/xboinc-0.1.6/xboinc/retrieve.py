# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import json

from .user import get_directory, get_domain
from .server.tools import untar
from .simulation_io import SimState, assert_versions


class RetrieveJobs:

    def __init__(self, user, study_name, dev_server=False):
        if not dev_server:
            raise NotImplementedError("Regular server not yet operational. "
                                    + "Please use dev_server=True.")
        assert_versions()
        self._study_name = study_name
        self._user = user
        self._domain = get_domain(user)
        if self._domain=='eos':
            missing_eos()
        if dev_server:
            self._directory = get_directory(user) / "output_dev"
        else:
            self._directory = get_directory(user) / "output"
        self._to_delete = []
        for tar_file in self._directory.glob('*.tar.gz'):
            untar(tar_file)


    def _clean(self):
        for json_file in self._to_delete:
            json_file.with_suffix('.bin').unlink()
            json_file.unlink()
        # Delete empty folders
        for folder in self._directory.glob('*/'):
            if not any(folder.iterdir()):
                folder.rmdir()


    def __iter__(self):
        json_files = []
        for json_file in self._directory.glob('*/*.json'):
            with open(json_file, 'r') as json_file_obj:
                json_content = json.load(json_file_obj)
            if json_content.get("study_name") == self._study_name \
            and json_content.get("user") == self._user:
                json_files.append(json_file)
        json_files = set(json_files) - set(self._to_delete)
        if not json_files:
            print(f"Warning: No JSON files found in {self._directory} for "
                + f"{self._user}, study_name {self._study_name}.")
        self._json_files = iter(json_files)
        return self


    def __next__(self):
        try:
            json_file = next(self._json_files)
        except StopIteration:
            self._clean()
            raise StopIteration
        else:
            bin_file = json_file.with_suffix('.bin')
            try:
                with open(json_file, 'r') as json_file_obj:
                    json_content = json.load(json_file_obj)
                result    = SimState.from_binary(bin_file)
                particles = result.particles
            except Exception as e:
                print(f"Error loading binary file {bin_file}: {e}")
            else: 
                self._to_delete.append(json_file)
                return particles, json_content

