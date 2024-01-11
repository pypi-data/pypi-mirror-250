// copyright ############################### #
// This file is part of the Xboinc Package.  #
// Copyright (c) CERN, 2023.                 #
// ######################################### #


#ifndef NULL
#define NULL 0
#endif

#ifndef COMPILE_TO_BOINC
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#endif

#include "xtrack_tracker.h"
#include "sim_config.h"

#define XB_INPUT_FILENAME "xboinc_input.bin"
#define XB_OUTPUT_FILENAME "sim_state_out.bin"
#define XB_CHECKPOINT_FILE "checkpoint.bin"


// ===============================================================================================
// IMPORTANT
// ===============================================================================================
// Only make changes to this file just before a minor version bump (need a separate commit though)
// to avoid having multiple xboinc versions with out-of-sync executables.

// ===============================================================================================
// Do not change
// ===============================================================================================
// version XXX.YYY as int  (no patch)
const int64_t xboinc_exec_version = 1;
// ===============================================================================================


int8_t run_slow = 0;
int8_t early_exit = 0;
int8_t early_crash = 0;
int8_t early_sleep = 0;
int8_t trickle_up = 0;
int8_t trickle_down = 0;
int8_t critical_section = 0;    // run most of the time in a critical section
int8_t report_fraction_done = 0;
int8_t network_usage = 0;
double cpu_time = 20, comp_result;


void    XB_fprintf(FILE *stream, char *format, ...);
FILE*   XB_fopen(char *filename, const char *mode);
FILE*   XB_fopen_allow_null(char *filename, const char *mode);
int8_t* XB_file_to_buffer(FILE *fid, int8_t *buf_in);
int     XB_do_checkpoint(SimConfig sim_config, SimStateData sim_state);


int main(int argc, char **argv){
    int retval, i;
#ifdef COMPILE_TO_BOINC
    // Parse BOINC arguments and initialise
    for (i=0; i<argc; i++) {
        if (strstr(argv[i], "early_exit")) early_exit = 1;
        if (strstr(argv[i], "early_crash")) early_crash = 1;
        if (strstr(argv[i], "early_sleep")) early_sleep = 1;
        if (strstr(argv[i], "run_slow")) run_slow = 1;
        if (strstr(argv[i], "critical_section")) critical_section = 1;
        if (strstr(argv[i], "network_usage")) network_usage = 1;
        if (strstr(argv[i], "cpu_time")) {
            cpu_time = atof(argv[++i]);
        }
        if (strstr(argv[i], "trickle_up")) trickle_up = 1;
        if (strstr(argv[i], "trickle_down")) trickle_down = 1;
    }
    retval = boinc_init();
    if (retval) {
        XB_fprintf(stderr, "Boinc_init returned %d\n", retval);
        exit(retval);
    }
    XB_fprintf(stdout, "App started; CPU time %f, flags:%s%s%s%s%s%s%s\n",
        cpu_time,
        early_exit?" early_exit":"",
        early_crash?" early_crash":"",
        early_sleep?" early_sleep":"",
        run_slow?" run_slow":"",
        critical_section?" critical_section":"",
        trickle_up?" trickle_up":"",
        trickle_down?" trickle_down":""
    );
    // TODO: What does this do?
    //       Should it go after loading the input file?
    //       Should it really hardcode the number of bytes like this...?
    if (network_usage) {
        boinc_network_usage(5., 17.);
    }
#endif

    // Open input file
    FILE* infile = XB_fopen(XB_INPUT_FILENAME, "rb");
    int8_t* sim_buffer = XB_file_to_buffer(infile, NULL);
    if (!sim_buffer){
        return -1;
    }

    // Get sim config and metadata
    SimConfig sim_config = (SimConfig) sim_buffer;
    const int64_t input_version = SimConfig_get_sim_state_version_xboinc_version(sim_config);
    if (input_version != xboinc_exec_version){
        XB_fprintf(stderr, "Xboinc version of executable and input file do not match!\n");
        return -1;
    }
    const int64_t num_turns = SimConfig_get_num_turns(sim_config);
    const int64_t num_elements = SimConfig_get_num_elements(sim_config);
    XB_fprintf(stdout, "num_turns: %d\n", (int) num_turns);
    XB_fprintf(stdout, "num_elements: %d\n", (int) num_elements);
    int64_t current_turn;
    ParticlesData particles = SimConfig_getp_sim_state_particles(sim_config);
    int64_t num_part = 0;
    for (int ii=0; ii<ParticlesData_get__capacity(particles); ii++){
        if(ParticlesData_get_state(particles, (int64_t) ii) > 0){
            num_part++;
        }
    }
    XB_fprintf(stdout, "num_part: %d\n", (int) num_part);
    SimStateData sim_state = SimConfig_getp_sim_state(sim_config);
    XB_fprintf(stdout, "sim_state: %p\n", (int8_t*) sim_state);
    const int64_t checkpoint_every = SimConfig_get_checkpoint_every(sim_config);

    // Check for checkpoint file and load if it exists, otherwise use SimState from input
    FILE* checkpoint_state = XB_fopen_allow_null(XB_CHECKPOINT_FILE, "rb");
    if (checkpoint_state){
        XB_file_to_buffer(checkpoint_state, (int8_t*) sim_state);
        current_turn = SimStateData_get_i_turn(sim_state);
        XB_fprintf(stdout, "Loaded checkpoint, continuing from turn %d.\n", (int) current_turn);
    } else {
        current_turn = SimStateData_get_i_turn(sim_state);
        XB_fprintf(stdout, "No checkpoint found, starting from turn %d.\n", (int) current_turn);
    }

    int64_t step_turns = 1;  // Seems to best solution to track one turn at a time, to allow BOINC to interrupt
    if (checkpoint_every > 0){
//         step_turns = checkpoint_every;
        printf("Checkpointing every %d turns.\n", (int) checkpoint_every);
    } else {
//         step_turns = num_turns;
        printf("Not checkpointing\n");
    }

    // Open output file as test
    FILE* outfile = XB_fopen(XB_OUTPUT_FILENAME, "wb");
    if (!outfile){
        return 1;
    }


    // Main loop  ================
    // ===========================
    while (current_turn < num_turns){
        track_line(
            sim_buffer, // int8_t* buffer,
            SimConfig_getp_line_metadata(sim_config), // ElementRefData elem_ref_data
            particles,          // ParticlesData particles,
            step_turns,         // int num_turns,
            0,                  // int ele_start,
            (int) num_elements, // int num_ele_track,
            1,    // int flag_end_turn_actions,
            1,    // int flag_reset_s_at_end_turn,
            0,    // int flag_monitor,
            0,    // int64_t num_ele_line, (needed only for backtracking)
            0.0,  // double line_length, (needed only for backtracking)
            NULL, // int8_t* buffer_tbt_monitor,
            0,    // int64_t offset_tbt_monitor
            NULL  // int8_t* io_buffer,
        );
        current_turn += step_turns;
        SimStateData_set_i_turn(sim_state, current_turn);

        if (
#ifdef COMPILE_TO_BOINC
        boinc_time_to_checkpoint() ||
#endif
        (checkpoint_every > 0 && current_turn % checkpoint_every == 0) ){
            retval = XB_do_checkpoint(sim_config, sim_state);
            if (retval) {
                XB_fprintf(stderr, "APP: xtrack checkpoint failed!\n");
                fclose(outfile);
                exit(retval);
            }
#ifdef COMPILE_TO_BOINC
            boinc_checkpoint_completed();
#endif
        }
#ifdef COMPILE_TO_BOINC
        if (report_fraction_done) {
            double fd = (int)current_turn / (int)num_turns;
            if (cpu_time) fd /= 2;
            boinc_fraction_done(fd);
        }
#endif
    }
    // End main loop  ===========
    // ==========================

    XB_fprintf(stdout, "Finished tracking\n");

    // Write output
    fwrite(SimConfig_getp_sim_state(sim_config), sizeof(int8_t),
           SimConfig_get_sim_state_size(sim_config), outfile);
    fclose(outfile);

#ifdef COMPILE_TO_BOINC
    // BOINC clean up
    if (trickle_up) {
        boinc_send_trickle_up(
            const_cast<char*>("example_app"),
            const_cast<char*>("sample trickle message")
        );
    }
    if (trickle_down) {
        boinc_sleep(10);
        char buf[256];
        retval = boinc_receive_trickle_down(buf, sizeof(buf));
        if (!retval) {
            fprintf(stderr, "Got trickle-down message: %s\n", buf);
        }
    }
    boinc_fraction_done(1);
    boinc_finish(0);
#endif

    // Remove checkpoint if still present
    checkpoint_state = XB_fopen_allow_null(XB_CHECKPOINT_FILE, "rb");
    if (checkpoint_state){
        fclose(checkpoint_state);
        if (remove(XB_CHECKPOINT_FILE) != 0){
            XB_fprintf(stderr, "Could not remove checkpoint file!\n");
        }
    }

    return 0;
}


void XB_fprintf(FILE *stream, char *format, ...) {
    va_list args;
    va_start(args, format);
#ifdef COMPILE_TO_BOINC
    char* buf = NULL;
    buf = boinc_msg_prefix(buf, 256*sizeof(char));
    fprintf(stream, "%s ", buf);
//     (char*)(retval + '')
#endif
    vfprintf(stream, format, args);
    va_end(args);
}


FILE* XB_fopen(char *filename, const char *mode){
    FILE *fid;
#ifdef COMPILE_TO_BOINC
    char resolved_name[512];
    boinc_resolve_filename(filename, resolved_name, sizeof(resolved_name));
    fid = boinc_fopen(resolved_name, mode);
#else
    fid = fopen(filename, mode);
#endif
    if (!fid) {
#ifdef COMPILE_TO_BOINC
        XB_fprintf(stderr, "APP: Could not open file %s (resolved name %s).\n",
            filename, resolved_name);
#else
        XB_fprintf(stderr, "Could not open file %s.\n",
            filename);
#endif
        return NULL;
    }
    return fid;
}


FILE* XB_fopen_allow_null(char *filename, const char *mode){
    FILE *fid;
#ifdef COMPILE_TO_BOINC
    char resolved_name[512];
    boinc_resolve_filename(filename, resolved_name, sizeof(resolved_name));
    fid = boinc_fopen(resolved_name, mode);
#else
    fid = fopen(filename, mode);
#endif
    return fid;
}


int8_t* XB_file_to_buffer(FILE *fid, int8_t *buf_in){
    if (!fid){
        return NULL;
    }
    // Get buffer
    int8_t *buf;
    fseek(fid, 0L, SEEK_END);
    unsigned long filesize = ftell(fid);
    fseek(fid, 0L, SEEK_SET);
    if (buf_in){
        XB_fprintf(stdout, "Reusing buffer.\n");
        buf = buf_in;
    } else {
        buf = (int8_t*)malloc(filesize*sizeof(int8_t));
    }
    fread(buf, sizeof(int8_t), filesize, fid);
    fclose(fid);
    if (!buf){
        XB_fprintf(stderr, "Could not allocate buffer!\n");
        return NULL;
    }
    return (buf);
}


int XB_do_checkpoint(SimConfig sim_config, SimStateData sim_state) {
    FILE *chkp_fid = XB_fopen(XB_CHECKPOINT_FILE, "wb");
    if (!chkp_fid) {
        return 1;
    }
    XB_fprintf(stdout, "Checkpointing turn %d\n", (int) SimStateData_get_i_turn(sim_state));
    fwrite(SimConfig_getp_sim_state(sim_config), sizeof(int8_t), SimConfig_get_sim_state_size(sim_config), chkp_fid);
    fclose(chkp_fid);
    return 0;
}
