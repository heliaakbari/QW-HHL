OPENQASM 2.0;
include "qelib1.inc";
gate unitary q0 { u(pi/2,pi/2,0) q0; }
gate multiplexer_dg q0 { unitary q0; }
gate unitary_131827110350800 q0 { u(pi/2,-2*pi,-pi/2) q0; }
gate unitary_131827110351056 q0 { u(0,3.5940583493700617,-2.0232620225751656) q0; }
gate multiplexer_dg_131827110084944 q0,q1 { unitary_131827110350800 q0; cx q1,q0; unitary_131827110351056 q0; }
gate unitary_131827110351440 q0 { u(pi/2,pi/4,2.8175392121489513) q0; }
gate unitary_131827110351824 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110352080 q0 { u(pi/2,-5*pi/4,-pi/2) q0; }
gate unitary_131827110352336 q0 { u(pi/2,-pi/2,-3*pi/2) q0; }
gate multiplexer_dg_131827110198736 q0,q1,q2 { unitary_131827110351440 q0; cx q1,q0; unitary_131827110351824 q0; cx q2,q0; unitary_131827110352080 q0; cx q1,q0; unitary_131827110352336 q0; }
gate unitary_131827110352592 q0 { u(pi/2,-2*pi,-pi/2) q0; }
gate unitary_131827110351696 q0 { u(pi/2,pi/2,-pi/2) q0; }
gate unitary_131827110352976 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110353232 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110353488 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110353872 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110354128 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110354384 q0 { u(pi/2,2.1694323292672673,-pi) q0; }
gate multiplexer_dg_131827110039888 q0,q1,q2,q3 { unitary_131827110352592 q0; cx q1,q0; unitary_131827110351696 q0; cx q2,q0; unitary_131827110352976 q0; cx q1,q0; unitary_131827110353232 q0; cx q3,q0; unitary_131827110353488 q0; cx q1,q0; unitary_131827110353872 q0; cx q2,q0; unitary_131827110354128 q0; cx q1,q0; unitary_131827110354384 q0; }
gate unitary_131827110353744 q0 { u(pi/2,pi/32,3.9346607209266713) q0; }
gate unitary_131827110354896 q0 { u(pi/4,pi/2,-1.4726215563702154) q0; }
gate unitary_131827110355280 q0 { u(3*pi/4,1.6689710972195773,3*pi/2) q0; }
gate unitary_131827110355664 q0 { u(0.9855826562165211,pi/2,4.81056375080937) q0; }
gate unitary_131827110302416 q0 { u(0.9855826562165237,-1.4726215563702154,-3*pi/2) q0; }
gate unitary_131827110306256 q0 { u(pi/4,-pi/2,1.6689710972195788) q0; }
gate unitary_131827110302160 q0 { u(3*pi/4,-1.4726215563702163,pi/2) q0; }
gate unitary_131827110085328 q0 { u(0.333640821365129,pi/2,-1.472621556370215) q0; }
gate unitary_131827110085968 q0 { u(2.807951832224666,1.86532063806894,3*pi/2) q0; }
gate unitary_131827110085456 q0 { u(3*pi/4,pi/2,5.006913291658733) q0; }
gate unitary_131827110086608 q0 { u(3*pi/4,-1.4726215563702159,pi/2) q0; }
gate unitary_131827110086992 q0 { u(pi/4,-pi/2,1.668971097219577) q0; }
gate unitary_131827110087248 q0 { u(pi/4,-4.614214209960011,-pi/2) q0; }
gate unitary_131827110089424 q0 { u(pi/4,-pi/2,1.6689710972195755) q0; }
gate unitary_131827110087760 q0 { u(pi/4,-4.417864669110648,-pi/2) q0; }
gate unitary_131827110088144 q0 { u(pi/2,-3*pi/2,3.4361169648638357) q0; }
gate multiplexer_dg_131827110039632 q0,q1,q2,q3,q4 { unitary_131827110353744 q0; cx q1,q0; unitary_131827110354896 q0; cx q2,q0; unitary_131827110355280 q0; cx q1,q0; unitary_131827110355664 q0; cx q3,q0; unitary_131827110302416 q0; cx q1,q0; unitary_131827110306256 q0; cx q2,q0; unitary_131827110302160 q0; cx q1,q0; unitary_131827110085328 q0; cx q4,q0; unitary_131827110085968 q0; cx q1,q0; unitary_131827110085456 q0; cx q2,q0; unitary_131827110086608 q0; cx q1,q0; unitary_131827110086992 q0; cx q3,q0; unitary_131827110087248 q0; cx q1,q0; unitary_131827110089424 q0; cx q2,q0; unitary_131827110087760 q0; cx q1,q0; unitary_131827110088144 q0; }
gate unitary_131827110088528 q0 { u(pi/2,-2*pi,-pi/2) q0; }
gate unitary_131827110088784 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110089040 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110089296 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110089936 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110090320 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110090576 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110090832 q0 { u(pi,-1.240240744746572,1.9013519088432216) q0; }
gate unitary_131827110091216 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110090192 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110091600 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110091856 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110092112 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110092368 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110092624 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110092880 q0 { u(pi,-7*pi/4,-3*pi/4) q0; }
gate unitary_131827110093264 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110093776 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110094288 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110094800 q0 { u(pi,-1.240240744746572,1.9013519088432216) q0; }
gate unitary_131827110095440 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110095952 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110096720 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110097360 q0 { u(3*pi/4,-3*pi/2,-pi/2) q0; }
gate unitary_131827110097872 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110098384 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110096848 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110099152 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110099664 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827136158032 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110473168 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110472912 q0 { u(pi/2,2.4666411069201106,-pi) q0; }
gate multiplexer_dg_131827110041424 q0,q1,q2,q3,q4,q5 { unitary_131827110088528 q0; cx q1,q0; unitary_131827110088784 q0; cx q2,q0; unitary_131827110089040 q0; cx q1,q0; unitary_131827110089296 q0; cx q3,q0; unitary_131827110089936 q0; cx q1,q0; unitary_131827110090320 q0; cx q2,q0; unitary_131827110090576 q0; cx q1,q0; unitary_131827110090832 q0; cx q4,q0; unitary_131827110091216 q0; cx q1,q0; unitary_131827110090192 q0; cx q2,q0; unitary_131827110091600 q0; cx q1,q0; unitary_131827110091856 q0; cx q3,q0; unitary_131827110092112 q0; cx q1,q0; unitary_131827110092368 q0; cx q2,q0; unitary_131827110092624 q0; cx q1,q0; unitary_131827110092880 q0; cx q5,q0; unitary_131827110093264 q0; cx q1,q0; unitary_131827110093776 q0; cx q2,q0; unitary_131827110094288 q0; cx q1,q0; unitary_131827110094800 q0; cx q3,q0; unitary_131827110095440 q0; cx q1,q0; unitary_131827110095952 q0; cx q2,q0; unitary_131827110096720 q0; cx q1,q0; unitary_131827110097360 q0; cx q4,q0; unitary_131827110097872 q0; cx q1,q0; unitary_131827110098384 q0; cx q2,q0; unitary_131827110096848 q0; cx q1,q0; unitary_131827110099152 q0; cx q3,q0; unitary_131827110099664 q0; cx q1,q0; unitary_131827136158032 q0; cx q2,q0; unitary_131827110473168 q0; cx q1,q0; unitary_131827110472912 q0; }
gate unitary_131827110472528 q0 { u(pi/2,-2*pi,-pi/2) q0; }
gate unitary_131827110472272 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110472016 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110471760 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110471504 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110471120 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110470864 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110470608 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110470352 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110471248 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110469968 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110469712 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110469456 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110469200 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110468944 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110468688 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110468432 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110468176 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110467920 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110467664 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110467408 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110467152 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110466896 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110466640 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110466384 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110466128 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110465872 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110465616 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110465360 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110465104 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110044880 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110050768 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110050512 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110050256 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110050000 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110049744 q0 { u(pi/2,pi/2,-pi/2) q0; }
gate unitary_131827110049488 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110048976 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110048592 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110048336 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110048080 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110047824 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110047568 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110047312 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110047056 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110041680 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110044496 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110044240 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110043984 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110043728 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110043472 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110043216 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110042960 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110042576 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110040912 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110040656 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827110040400 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827110040144 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827109964624 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827109964112 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827109963600 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827109963088 q0 { u(pi/2,-3*pi/2,-pi/2) q0; }
gate unitary_131827109962576 q0 { u(pi/2,-pi/2,pi/2) q0; }
gate unitary_131827109962064 q0 { u(pi/2,-pi/8,pi) q0; }
gate multiplexer_dg_131827110051280 q0,q1,q2,q3,q4,q5,q6 { unitary_131827110472528 q0; cx q1,q0; unitary_131827110472272 q0; cx q2,q0; unitary_131827110472016 q0; cx q1,q0; unitary_131827110471760 q0; cx q3,q0; unitary_131827110471504 q0; cx q1,q0; unitary_131827110471120 q0; cx q2,q0; unitary_131827110470864 q0; cx q1,q0; unitary_131827110470608 q0; cx q4,q0; unitary_131827110470352 q0; cx q1,q0; unitary_131827110471248 q0; cx q2,q0; unitary_131827110469968 q0; cx q1,q0; unitary_131827110469712 q0; cx q3,q0; unitary_131827110469456 q0; cx q1,q0; unitary_131827110469200 q0; cx q2,q0; unitary_131827110468944 q0; cx q1,q0; unitary_131827110468688 q0; cx q5,q0; unitary_131827110468432 q0; cx q1,q0; unitary_131827110468176 q0; cx q2,q0; unitary_131827110467920 q0; cx q1,q0; unitary_131827110467664 q0; cx q3,q0; unitary_131827110467408 q0; cx q1,q0; unitary_131827110467152 q0; cx q2,q0; unitary_131827110466896 q0; cx q1,q0; unitary_131827110466640 q0; cx q4,q0; unitary_131827110466384 q0; cx q1,q0; unitary_131827110466128 q0; cx q2,q0; unitary_131827110465872 q0; cx q1,q0; unitary_131827110465616 q0; cx q3,q0; unitary_131827110465360 q0; cx q1,q0; unitary_131827110465104 q0; cx q2,q0; unitary_131827110044880 q0; cx q1,q0; unitary_131827110050768 q0; cx q6,q0; unitary_131827110050512 q0; cx q1,q0; unitary_131827110050256 q0; cx q2,q0; unitary_131827110050000 q0; cx q1,q0; unitary_131827110049744 q0; cx q3,q0; unitary_131827110049488 q0; cx q1,q0; unitary_131827110048976 q0; cx q2,q0; unitary_131827110048592 q0; cx q1,q0; unitary_131827110048336 q0; cx q4,q0; unitary_131827110048080 q0; cx q1,q0; unitary_131827110047824 q0; cx q2,q0; unitary_131827110047568 q0; cx q1,q0; unitary_131827110047312 q0; cx q3,q0; unitary_131827110047056 q0; cx q1,q0; unitary_131827110041680 q0; cx q2,q0; unitary_131827110044496 q0; cx q1,q0; unitary_131827110044240 q0; cx q5,q0; unitary_131827110043984 q0; cx q1,q0; unitary_131827110043728 q0; cx q2,q0; unitary_131827110043472 q0; cx q1,q0; unitary_131827110043216 q0; cx q3,q0; unitary_131827110042960 q0; cx q1,q0; unitary_131827110042576 q0; cx q2,q0; unitary_131827110040912 q0; cx q1,q0; unitary_131827110040656 q0; cx q4,q0; unitary_131827110040400 q0; cx q1,q0; unitary_131827110040144 q0; cx q2,q0; unitary_131827109964624 q0; cx q1,q0; unitary_131827109964112 q0; cx q3,q0; unitary_131827109963600 q0; cx q1,q0; unitary_131827109963088 q0; cx q2,q0; unitary_131827109962576 q0; cx q1,q0; unitary_131827109962064 q0; }
gate isometry_to_uncompute_dg q0,q1,q2,q3,q4,q5,q6 { multiplexer_dg q6; multiplexer_dg_131827110084944 q5,q6; multiplexer_dg_131827110198736 q4,q5,q6; multiplexer_dg_131827110039888 q3,q4,q5,q6; multiplexer_dg_131827110039632 q2,q3,q4,q5,q6; multiplexer_dg_131827110041424 q1,q2,q3,q4,q5,q6; multiplexer_dg_131827110051280 q0,q1,q2,q3,q4,q5,q6; }
gate state_preparation(param0,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,param13,param14,param15,param16,param17,param18,param19,param20,param21,param22,param23,param24,param25,param26,param27,param28,param29,param30,param31,param32,param33,param34,param35,param36,param37,param38,param39,param40,param41,param42,param43,param44,param45,param46,param47,param48,param49,param50,param51,param52,param53,param54,param55,param56,param57,param58,param59,param60,param61,param62,param63,param64,param65,param66,param67,param68,param69,param70,param71,param72,param73,param74,param75,param76,param77,param78,param79,param80,param81,param82,param83,param84,param85,param86,param87,param88,param89,param90,param91,param92,param93,param94,param95,param96,param97,param98,param99,param100,param101,param102,param103,param104,param105,param106,param107,param108,param109,param110,param111,param112,param113,param114,param115,param116,param117,param118,param119,param120,param121,param122,param123,param124,param125,param126,param127) q0,q1,q2,q3,q4,q5,q6 { isometry_to_uncompute_dg q0,q1,q2,q3,q4,q5,q6; }
gate ccx_o1 q0,q1,q2 { x q1; ccx q0,q1,q2; x q1; }
gate ccz q0,q1,q2 { h q2; ccx q0,q1,q2; h q2; }
gate ccz_o1 q0,q1,q2 { x q1; ccz q0,q1,q2; x q1; }
gate cch q0,q1,q2 { s q2; h q2; t q2; ccx q0,q1,q2; tdg q2; h q2; sdg q2; }
gate cch_o1 q0,q1,q2 { x q1; cch q0,q1,q2; x q1; }
qreg a_hhl[1];
qreg r2a[1];
qreg r2[1];
qreg r1a[1];
qreg r1[1];
qreg phase[2];
state_preparation(0.3535533905932732,0,0,0,0.3535533905932731,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.35355339059327306j,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.35355339059327306j,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2499999999999996j,0,0,0,0.2499999999999996j,0,0,0,0,0,0,0,0,0,0,0,0.24999999999999953j,0,0,0,0.24999999999999953j,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-0.4999999999999991,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) a_hhl[0],r2a[0],r2[0],r1a[0],r1[0],phase[0],phase[1];
ccx phase[1],r1a[0],r2a[0];
cz phase[1],r2[0];
cx phase[1],r2[0];
cz phase[1],r2[0];
cx phase[1],r2[0];
ccx_o1 phase[1],r2[0],r2a[0];
ccz_o1 phase[1],r2[0],r2a[0];
ccx_o1 phase[1],r2[0],r2a[0];
cch_o1 phase[1],r1a[0],r2[0];
