// copyright ############################### #
// This file is part of the Xboinc Package.  #
// Copyright (c) CERN, 2023.                 #
// ######################################### #


// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2008 University of California
//
// BOINC is free software; you can redistribute it and/or modify it
// under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation,
// either version 3 of the License, or (at your option) any later version.
//
// BOINC is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with BOINC.  If not, see <http://www.gnu.org/licenses/>.

// command line options
// --cpu_time N: use about N CPU seconds after copying files
// --critical_section: run most of the time in a critical section
// --early_exit: exit(10) after 30 chars
// --early_crash: crash after 30 chars
// --run_slow: sleep 1 second after each character
// --trickle_up: sent a trickle-up message
// --trickle_down: receive a trickle-up message
// --network_usage: tell the client we used some network

// #include <stdio.h>
// #ifndef NULL
//     #define NULL 0
// #endif
// #include <stdlib.h>
// #include <math.h>

#ifdef _WIN32
#include "boinc_win.h"
#else
#include "config.h"
#include <cstdio>
#include <cctype>
#include <ctime>
#include <cstring>
#include <cstdlib>
#include <csignal>
#include <cstdarg>
#include <cmath>
#include <unistd.h>
#endif

#include "str_util.h"
#include "util.h"
#include "filesys.h"
#include "boinc_api.h"
#include "mfile.h"
#include "graphics2.h"

struct UC_SHMEM {
    double update_time;
    double fraction_done;
    double cpu_time;
    BOINC_STATUS status;
    int countdown;
        // graphics app sets this to 5 repeatedly,
        // main program decrements it once/sec.
        // If it's zero, don't bother updating shmem
};

#ifdef _WIN32

extern "C" {

__declspec( dllimport )  char* xtrack_dll_version();

};

#endif

#include <iostream>

#ifdef APP_GRAPHICS
UC_SHMEM* shmem;
#endif

using std::string;
