OPENQASM 2.0;
include "qelib1.inc";
gate isometry_to_uncompute_dg q0,q1,q2,q3,q4,q5,q6 {  }
gate state_preparation(param0,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,param13,param14,param15,param16,param17,param18,param19,param20,param21,param22,param23,param24,param25,param26,param27,param28,param29,param30,param31,param32,param33,param34,param35,param36,param37,param38,param39,param40,param41,param42,param43,param44,param45,param46,param47,param48,param49,param50,param51,param52,param53,param54,param55,param56,param57,param58,param59,param60,param61,param62,param63,param64,param65,param66,param67,param68,param69,param70,param71,param72,param73,param74,param75,param76,param77,param78,param79,param80,param81,param82,param83,param84,param85,param86,param87,param88,param89,param90,param91,param92,param93,param94,param95,param96,param97,param98,param99,param100,param101,param102,param103,param104,param105,param106,param107,param108,param109,param110,param111,param112,param113,param114,param115,param116,param117,param118,param119,param120,param121,param122,param123,param124,param125,param126,param127) q0,q1,q2,q3,q4,q5,q6 { isometry_to_uncompute_dg q0,q1,q2,q3,q4,q5,q6; }
gate cch q0,q1,q2 { s q2; h q2; t q2; ccx q0,q1,q2; tdg q2; h q2; sdg q2; }
gate cch_o1 q0,q1,q2 { x q1; cch q0,q1,q2; x q1; }
gate ccx_o1 q0,q1,q2 { x q1; ccx q0,q1,q2; x q1; }
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
gate ccz_o1 q0,q1,q2 { x q1; ccz q0,q1,q2; x q1; }
gate cs q0,q1 { t q0; cx q0,q1; tdg q1; cx q0,q1; t q1; }
qreg a_hhl[1];
qreg r2a[1];
qreg r2[1];
qreg r1a[1];
qreg r1[1];
qreg phase[2];
state_preparation(1.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) a_hhl[0],r2a[0],r2[0],r1a[0],r1[0],phase[0],phase[1];
h r2[0];
barrier a_hhl[0],r2a[0],r2[0],r1a[0],r1[0],phase[0],phase[1];
h phase[0];
h phase[1];
cch_o1 phase[0],r1a[0],r2[0];
ccx phase[0],r1a[0],r2a[0];
cz phase[0],r2[0];
cx phase[0],r2[0];
cz phase[0],r2[0];
cx phase[0],r2[0];
ccx_o1 phase[0],r2[0],r2a[0];
ccz_o1 phase[0],r2[0],r2a[0];
ccx_o1 phase[0],r2[0],r2a[0];
cch_o1 phase[0],r1a[0],r2[0];
ccx phase[0],r1a[0],r2a[0];
cswap phase[0],r1[0],r2[0];
cswap phase[0],r1a[0],r2a[0];
cs phase[0],r1[0];
cx phase[0],r1[0];
cs phase[0],r1[0];
cx phase[0],r1[0];
cch_o1 phase[1],r1a[0],r2[0];
ccx phase[1],r1a[0],r2a[0];
cz phase[1],r2[0];
cx phase[1],r2[0];
cz phase[1],r2[0];
cx phase[1],r2[0];
ccx_o1 phase[1],r2[0],r2a[0];
ccz_o1 phase[1],r2[0],r2a[0];
ccx_o1 phase[1],r2[0],r2a[0];
cch_o1 phase[1],r1a[0],r2[0];
ccx phase[1],r1a[0],r2a[0];
cswap phase[1],r1[0],r2[0];
cswap phase[1],r1a[0],r2a[0];
cs phase[1],r1[0];
cx phase[1],r1[0];
cs phase[1],r1[0];
cx phase[1],r1[0];
cch_o1 phase[1],r1a[0],r2[0];
