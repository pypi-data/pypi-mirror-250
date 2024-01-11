# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import xobjects as xo
from ..simulation_io import SimState, SimConfig, SimVersion, app_version, get_default_tracker, assert_versions
from ..general import _pkg_root, __version__

from pathlib import Path
import shutil
import subprocess

# ===============================================================================================
# IMPORTANT
# ===============================================================================================
# Only make changes to this file just before a minor version bump (need a separate commit though)
# to avoid having multiple xboinc versions with out-of-sync executables.
# ===============================================================================================

insert_in_all_files = """
#include <stdio.h>
#ifndef NULL
    #define NULL 0
#endif
"""

def generate_executable_source(*, write_source_files=True, _context=None):
    assert _context is None
    assert write_source_files
    assert_versions()

    sim_config_sources = [
        insert_in_all_files,
        xo.specialize_source(SimVersion._XoStruct._gen_c_api().source,
                                    specialize_for='cpu_serial'),
        xo.specialize_source(SimState._XoStruct._gen_c_api().source,
                                    specialize_for='cpu_serial'),
        xo.specialize_source(SimConfig._gen_c_api().source,
                                    specialize_for='cpu_serial'),
    ]

    sim_config_h = '\n'.join(sim_config_sources)

    default_tracker, default_config_hash = get_default_tracker()
    track_kernel = default_tracker.track_kernel[default_config_hash]
    xtrack_tracker_h = (
        insert_in_all_files + track_kernel.specialized_source)

    with open(_pkg_root.joinpath('executable/main.c'), 'r') as fid:
        main_c = insert_in_all_files + fid.read()

    dct_sources = {
        'sim_config.h': sim_config_h,
        'xtrack_tracker.h': xtrack_tracker_h,
        'main.c': main_c,
    }

    for nn, vv in dct_sources.items():
        file = Path.cwd() / nn
        with file.open('w') as fid:
            fid.write(vv)

    return dct_sources


# BOINC executable naming conventions:
# windows_intelx86            Microsoft Windows (98 or later) running on an Intel x86-compatible CPU   (32bit)
# windows_x86_64              Microsoft Windows running on an AMD x86_64 or Intel EM64T CPU
# i686-pc-linux-gnu           Linux running on an Intel x86-compatible CPU    (32bit)
# x86_64-pc-linux-gnu         Linux running on an AMD x86_64 or Intel EM64T CPU
# powerpc-apple-darwin        Mac OS X 10.3 or later running on Motorola PowerPC
# i686-apple-darwin           Mac OS 10.4 or later running on Intel   (32bit)
# x86_64-apple-darwin         Intel 64-bit Mac OS 10.5 or later
# arm64-apple-darwin          Mac OS on M1 or M2
# sparc-sun-solaris2.7        Solaris 2.7 running on a SPARC-compatible CPU
# sparc-sun-solaris           Solaris 2.8 or later running on a SPARC-compatible CPU
# sparc64-sun-solaris         Solaris 2.8 or later running on a SPARC 64-bit CPU
# powerpc64-ps3-linux-gnu     Sony Playstation 3 running Linux
# arm-android-linux-gnu       Android running on ARM
# aarch64-android-linux-gnu   Android running on aarch64 
# aarch64-unknown-linux-gnu   Linux running aarch64
# x86_64-pc-freebsd__sse2     Free BSD running on 64 bit X86

def generate_executable(*, keep_source=False, windows32=False, windows64=False):
    assert_versions()
    main    = Path.cwd() / "main.c"
    config  = Path.cwd() / "sim_config.h"
    tracker = Path.cwd() / "xtrack_tracker.h"
    if not main.exists() or not config.exists() or not tracker.exists():
        source_files = generate_executable_source()

    tag = f'_{app_version}'
    if windows64:
        if shutil.which("x86_64-w64-mingw32-gcc") is not None:
            compiler = "x86_64-w64-mingw32-gcc"
        else:
            raise ValueError("Mingw32 not found!")
        tag += '-windows_x86_64.exe'
    elif windows32:
        if shutil.which("i686-w64-mingw32-gcc") is not None:
            compiler = "i686-w64-mingw32-gcc"
        else:
            raise ValueError("Mingw32 not found!")
        tag += '-windows_intelx86.exe'
    else:
        if shutil.which("gcc") is not None:
            compiler = "gcc"
        elif shutil.which("clang") is not None:
            compiler = "clang"
        else:
            raise RuntimeError("Neither clang or gcc are found. Install a C compiler.")
        cmd = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE)
        if cmd.returncode == 0:
            machine = cmd.stdout.decode('UTF-8').strip().lower()
        cmd = subprocess.run(['uname', '-s'], stdout=subprocess.PIPE)
        if cmd.returncode == 0:
            thisos = cmd.stdout.decode('UTF-8').strip().lower()
        vendor = 'apple' if thisos=='darwin' else 'pc'
        thisos = f'{thisos}-gnu' if thisos=='linux' else thisos
        tag += f"-{machine}-{vendor}-{thisos}"

    cmd = subprocess.run([compiler, 'main.c', '-O3', '-o', f'xboinc{tag}', '-lm'],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cmd.returncode != 0:
        stderr = cmd.stderr.decode('UTF-8').strip().split('\n')
        raise RuntimeError(f"Compilation failed. Stderr:\n {stderr}")

    if keep_source:
        main.rename(main.parent / f'{main.stem}{tag}{main.suffix}')
        config.rename(config.parent / f'{config.stem}{tag}{config.suffix}')
        tracker.rename(tracker.parent / f'{tracker.stem}{tag}{tracker.suffix}')
    else:
        main.unlink()
        config.unlink()
        tracker.unlink()
