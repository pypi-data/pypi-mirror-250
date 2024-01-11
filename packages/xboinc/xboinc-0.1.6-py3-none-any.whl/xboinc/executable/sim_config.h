
#include <stdio.h>
#ifndef NULL
    #define NULL 0
#endif

#ifndef XOBJ_TYPEDEF_SimVersionData
#define XOBJ_TYPEDEF_SimVersionData
typedef   struct SimVersionData_s * SimVersionData;
 static inline SimVersionData SimVersionData_getp(SimVersionData  obj){
  int64_t offset=0;
  return (SimVersionData)(( char*) obj+offset);
}
 static inline int64_t SimVersionData_get_xboinc_version(const SimVersionData  obj){
  int64_t offset=0;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimVersionData_set_xboinc_version(SimVersionData  obj, int64_t value){
  int64_t offset=0;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimVersionData_getp_xboinc_version(SimVersionData  obj){
  int64_t offset=0;
  return ( int64_t*)(( char*) obj+offset);
}
#endif
#ifndef XOBJ_TYPEDEF_SimStateData
#define XOBJ_TYPEDEF_SimStateData
typedef   struct SimStateData_s * SimStateData;
 static inline SimStateData SimStateData_getp(SimStateData  obj){
  int64_t offset=0;
  return (SimStateData)(( char*) obj+offset);
}
 static inline SimVersionData SimStateData_getp_version(SimStateData  obj){
  int64_t offset=0;
  offset+=8;
  return (SimVersionData)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_version_xboinc_version(const SimStateData  obj){
  int64_t offset=0;
  offset+=8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_version_xboinc_version(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_version_xboinc_version(SimStateData  obj){
  int64_t offset=0;
  offset+=8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_i_turn(const SimStateData  obj){
  int64_t offset=0;
  offset+=16;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_i_turn(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=16;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_i_turn(SimStateData  obj){
  int64_t offset=0;
  offset+=16;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_size(const SimStateData  obj){
  int64_t offset=0;
  offset+=24;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_size(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=24;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_size(SimStateData  obj){
  int64_t offset=0;
  offset+=24;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ParticlesData SimStateData_getp_particles(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  return (ParticlesData)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_particles__capacity(const SimStateData  obj){
  int64_t offset=0;
  offset+=40;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__capacity(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=40;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_particles__capacity(SimStateData  obj){
  int64_t offset=0;
  offset+=40;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_particles__num_active_particles(const SimStateData  obj){
  int64_t offset=0;
  offset+=48;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__num_active_particles(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=48;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_particles__num_active_particles(SimStateData  obj){
  int64_t offset=0;
  offset+=48;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_particles__num_lost_particles(const SimStateData  obj){
  int64_t offset=0;
  offset+=56;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__num_lost_particles(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=56;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_particles__num_lost_particles(SimStateData  obj){
  int64_t offset=0;
  offset+=56;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimStateData_get_particles_start_tracking_at_element(const SimStateData  obj){
  int64_t offset=0;
  offset+=64;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_start_tracking_at_element(SimStateData  obj, int64_t value){
  int64_t offset=0;
  offset+=64;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp_particles_start_tracking_at_element(SimStateData  obj){
  int64_t offset=0;
  offset+=64;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline double SimStateData_get_particles_q0(const SimStateData  obj){
  int64_t offset=0;
  offset+=72;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_q0(SimStateData  obj, double value){
  int64_t offset=0;
  offset+=72;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp_particles_q0(SimStateData  obj){
  int64_t offset=0;
  offset+=72;
  return ( double*)(( char*) obj+offset);
}
 static inline double SimStateData_get_particles_mass0(const SimStateData  obj){
  int64_t offset=0;
  offset+=80;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_mass0(SimStateData  obj, double value){
  int64_t offset=0;
  offset+=80;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp_particles_mass0(SimStateData  obj){
  int64_t offset=0;
  offset+=80;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_p0c(SimStateData  obj){
  int64_t offset=0;
  offset+=280;
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_p0c(SimStateData  obj){
  int64_t offset=0;
  offset+=280;
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_p0c(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=280;
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_p0c(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=280;
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_p0c(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=280;
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_gamma0(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_gamma0(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_gamma0(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_gamma0(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_gamma0(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_beta0(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_beta0(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_beta0(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_beta0(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_beta0(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_s(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_s(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_s(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_s(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_s(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_zeta(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_zeta(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_zeta(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_zeta(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_zeta(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_ptau(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_ptau(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_ptau(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_ptau(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_ptau(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_delta(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_delta(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_delta(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_delta(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_delta(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_rpp(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_rpp(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_rpp(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_rpp(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_rpp(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_rvv(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_rvv(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_rvv(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_rvv(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_rvv(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_chi(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_chi(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_chi(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_chi(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_chi(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_charge_ratio(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_charge_ratio(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_charge_ratio(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_charge_ratio(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_charge_ratio(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_weight(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_weight(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_weight(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_weight(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_weight(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimStateData_getp_particles_particle_id(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_particle_id(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimStateData_get_particles_particle_id(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_particle_id(SimStateData  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp1_particles_particle_id(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimStateData_getp_particles_at_element(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_at_element(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimStateData_get_particles_at_element(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_at_element(SimStateData  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp1_particles_at_element(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimStateData_getp_particles_at_turn(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_at_turn(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimStateData_get_particles_at_turn(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_at_turn(SimStateData  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp1_particles_at_turn(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimStateData_getp_particles_state(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_state(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimStateData_get_particles_state(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_state(SimStateData  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp1_particles_state(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimStateData_getp_particles_parent_particle_id(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_parent_particle_id(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimStateData_get_particles_parent_particle_id(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_parent_particle_id(SimStateData  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimStateData_getp1_particles_parent_particle_id(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimStateData_getp_particles__rng_s1(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles__rng_s1(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimStateData_get_particles__rng_s1(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__rng_s1(SimStateData  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimStateData_getp1_particles__rng_s1(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimStateData_getp_particles__rng_s2(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles__rng_s2(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimStateData_get_particles__rng_s2(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__rng_s2(SimStateData  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimStateData_getp1_particles__rng_s2(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimStateData_getp_particles__rng_s3(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles__rng_s3(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimStateData_get_particles__rng_s3(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__rng_s3(SimStateData  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimStateData_getp1_particles__rng_s3(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimStateData_getp_particles__rng_s4(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles__rng_s4(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimStateData_get_particles__rng_s4(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles__rng_s4(SimStateData  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimStateData_getp1_particles__rng_s4(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_x(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_x(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_x(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_x(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_x(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_y(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_y(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_y(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_y(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_y(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_px(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_px(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_px(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_px(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_px(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimStateData_getp_particles_py(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimStateData_len_particles_py(SimStateData  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimStateData_get_particles_py(const SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimStateData_set_particles_py(SimStateData  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimStateData_getp1_particles_py(SimStateData  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
#endif
#ifndef XOBJ_TYPEDEF_SimConfig
#define XOBJ_TYPEDEF_SimConfig
typedef   struct SimConfig_s * SimConfig;
 static inline SimConfig SimConfig_getp(SimConfig  obj){
  int64_t offset=0;
  return (SimConfig)(( char*) obj+offset);
}
 static inline ElementRefData SimConfig_getp_line_metadata(SimConfig  obj){
  int64_t offset=0;
  offset+=*( int64_t*)(( char*) obj+offset);
  return (ElementRefData)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_num_turns(const SimConfig  obj){
  int64_t offset=0;
  offset+=8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_num_turns(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_num_turns(SimConfig  obj){
  int64_t offset=0;
  offset+=8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_num_elements(const SimConfig  obj){
  int64_t offset=0;
  offset+=16;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_num_elements(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=16;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_num_elements(SimConfig  obj){
  int64_t offset=0;
  offset+=16;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_checkpoint_every(const SimConfig  obj){
  int64_t offset=0;
  offset+=24;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_checkpoint_every(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=24;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_checkpoint_every(SimConfig  obj){
  int64_t offset=0;
  offset+=24;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline SimStateData SimConfig_getp_sim_state(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  return (SimStateData)(( char*) obj+offset);
}
 static inline SimVersionData SimConfig_getp_sim_state_version(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=8;
  return (SimVersionData)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_version_xboinc_version(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_version_xboinc_version(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_version_xboinc_version(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_i_turn(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=16;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_i_turn(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=16;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_i_turn(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=16;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_size(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=24;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_size(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=24;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_size(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=24;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ParticlesData SimConfig_getp_sim_state_particles(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  return (ParticlesData)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_particles__capacity(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=40;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__capacity(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=40;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_particles__capacity(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=40;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_particles__num_active_particles(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=48;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__num_active_particles(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=48;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_particles__num_active_particles(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=48;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_particles__num_lost_particles(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=56;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__num_lost_particles(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=56;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_particles__num_lost_particles(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=56;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline int64_t SimConfig_get_sim_state_particles_start_tracking_at_element(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=64;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_start_tracking_at_element(SimConfig  obj, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=64;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp_sim_state_particles_start_tracking_at_element(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=64;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline double SimConfig_get_sim_state_particles_q0(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=72;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_q0(SimConfig  obj, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=72;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp_sim_state_particles_q0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=72;
  return ( double*)(( char*) obj+offset);
}
 static inline double SimConfig_get_sim_state_particles_mass0(const SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=80;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_mass0(SimConfig  obj, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=80;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp_sim_state_particles_mass0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=80;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_p0c(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=280;
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_p0c(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=280;
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_p0c(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=280;
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_p0c(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=280;
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_p0c(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=280;
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_gamma0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_gamma0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_gamma0(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_gamma0(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_gamma0(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+56);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_beta0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_beta0(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_beta0(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_beta0(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_beta0(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+64);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_s(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_s(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_s(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_s(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_s(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+72);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_zeta(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_zeta(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_zeta(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_zeta(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_zeta(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+80);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_ptau(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_ptau(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_ptau(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_ptau(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_ptau(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+88);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_delta(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_delta(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_delta(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_delta(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_delta(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+96);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_rpp(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_rpp(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_rpp(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_rpp(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_rpp(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+104);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_rvv(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_rvv(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_rvv(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_rvv(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_rvv(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+112);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_chi(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_chi(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_chi(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_chi(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_chi(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+120);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_charge_ratio(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_charge_ratio(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_charge_ratio(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_charge_ratio(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_charge_ratio(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+128);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_weight(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_weight(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_weight(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_weight(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_weight(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+136);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimConfig_getp_sim_state_particles_particle_id(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_particle_id(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimConfig_get_sim_state_particles_particle_id(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_particle_id(SimConfig  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp1_sim_state_particles_particle_id(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+144);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimConfig_getp_sim_state_particles_at_element(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_at_element(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimConfig_get_sim_state_particles_at_element(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_at_element(SimConfig  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp1_sim_state_particles_at_element(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+152);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimConfig_getp_sim_state_particles_at_turn(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_at_turn(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimConfig_get_sim_state_particles_at_turn(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_at_turn(SimConfig  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp1_sim_state_particles_at_turn(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+160);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimConfig_getp_sim_state_particles_state(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_state(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimConfig_get_sim_state_particles_state(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_state(SimConfig  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp1_sim_state_particles_state(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+168);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNInt64 SimConfig_getp_sim_state_particles_parent_particle_id(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  return (ArrNInt64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_parent_particle_id(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline int64_t SimConfig_get_sim_state_particles_parent_particle_id(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  return *( int64_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_parent_particle_id(SimConfig  obj, int64_t i0, int64_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  *( int64_t*)(( char*) obj+offset)=value;
}
 static inline  int64_t* SimConfig_getp1_sim_state_particles_parent_particle_id(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+176);
  offset+=16+i0*8;
  return ( int64_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimConfig_getp_sim_state_particles__rng_s1(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles__rng_s1(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimConfig_get_sim_state_particles__rng_s1(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__rng_s1(SimConfig  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimConfig_getp1_sim_state_particles__rng_s1(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+184);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimConfig_getp_sim_state_particles__rng_s2(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles__rng_s2(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimConfig_get_sim_state_particles__rng_s2(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__rng_s2(SimConfig  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimConfig_getp1_sim_state_particles__rng_s2(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+192);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimConfig_getp_sim_state_particles__rng_s3(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles__rng_s3(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimConfig_get_sim_state_particles__rng_s3(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__rng_s3(SimConfig  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimConfig_getp1_sim_state_particles__rng_s3(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+200);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNUint32 SimConfig_getp_sim_state_particles__rng_s4(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  return (ArrNUint32)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles__rng_s4(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline uint32_t SimConfig_get_sim_state_particles__rng_s4(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  return *( uint32_t*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles__rng_s4(SimConfig  obj, int64_t i0, uint32_t value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  *( uint32_t*)(( char*) obj+offset)=value;
}
 static inline  uint32_t* SimConfig_getp1_sim_state_particles__rng_s4(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+208);
  offset+=16+i0*4;
  return ( uint32_t*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_x(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_x(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_x(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_x(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_x(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+216);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_y(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_y(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_y(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_y(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_y(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+224);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_px(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_px(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_px(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_px(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_px(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+232);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
 static inline ArrNFloat64 SimConfig_getp_sim_state_particles_py(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  return (ArrNFloat64)(( char*) obj+offset);
}
 static inline int64_t SimConfig_len_sim_state_particles_py(SimConfig  obj){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
   int64_t* arr = ( int64_t*)(( char*) obj+offset);
  return arr[1];
}
 static inline double SimConfig_get_sim_state_particles_py(const SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  return *( double*)(( char*) obj+offset);
}
 static inline void SimConfig_set_sim_state_particles_py(SimConfig  obj, int64_t i0, double value){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  *( double*)(( char*) obj+offset)=value;
}
 static inline  double* SimConfig_getp1_sim_state_particles_py(SimConfig  obj, int64_t i0){
  int64_t offset=0;
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset);
  offset+=32;
  offset+=*( int64_t*)(( char*) obj+offset+240);
  offset+=16+i0*8;
  return ( double*)(( char*) obj+offset);
}
#endif