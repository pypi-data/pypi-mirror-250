V34 :0x24 hipfort_auxiliary
106 /long_pathname_so_that_rpms_can_package_the_debug_info/src/extlibs/hipFORT/lib/hipfort/hipfort_auxiliary.f S668 0
12/12/2023  21:22:51
use iso_c_binding private
use hipfort_types private
enduse
D 60 20 12
D 62 26 696 8 695 7
D 71 26 699 8 698 7
D 92 26 1367 12 1366 3
D 101 26 1373 1048 1372 7
S 668 24 0 0 0 9 1 0 5301 10005 0 A 0 0 0 0 B 0 1 0 0 0 0 0 0 0 0 0 0 38 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 hipfort_auxiliary
S 669 19 0 0 0 9 1 668 5319 4000 0 A 0 0 0 0 B 0 15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 1 0 0 0 0 0 668 0 0 0 0 hipgetdeviceproperties
O 669 1 670
S 670 14 5 0 0 6 1 668 5342 4 18000 A 1000000 0 0 0 B 0 19 0 0 0 0 0 2 2 0 0 675 0 0 0 0 0 0 0 0 0 19 0 668 0 0 674 0 hipgetdeviceproperties_
F 670 2 671 672
S 671 1 3 2 0 101 1 670 5366 2004 2000 A 0 0 0 0 B 0 19 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 prop
S 672 1 3 0 0 6 1 670 5371 2004 6000 A 0 0 0 0 B 0 19 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 deviceid
S 673 3 0 0 0 6 1 1 0 0 0 A 0 0 0 0 B 0 0 0 0 0 0 0 0 0 22 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6
S 674 3 0 0 0 60 0 1 0 0 0 A 0 0 0 0 B 0 0 0 0 0 0 0 0 5380 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 20 22 68 69 70 47 65 74 44 65 76 69 63 65 50 72 6f 70 65 72 74 69 65 73
S 675 1 3 0 0 6 1 670 5342 2004 1002000 A 0 0 0 0 B 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 hipgetdeviceproperties_
R 695 25 6 iso_c_binding c_ptr
R 696 5 7 iso_c_binding val c_ptr
R 698 25 9 iso_c_binding c_funptr
R 699 5 10 iso_c_binding val c_funptr
R 733 6 44 iso_c_binding c_null_ptr$ac
R 735 6 46 iso_c_binding c_null_funptr$ac
R 736 26 47 iso_c_binding ==
R 738 26 49 iso_c_binding !=
R 1366 25 1 hipfort_types dim3
R 1367 5 2 hipfort_types x dim3
R 1368 5 3 hipfort_types y dim3
R 1369 5 4 hipfort_types z dim3
R 1372 25 7 hipfort_types hipdeviceprop_t
R 1373 5 8 hipfort_types name hipdeviceprop_t
R 1374 5 9 hipfort_types totalglobalmem hipdeviceprop_t
R 1375 5 10 hipfort_types sharedmemperblock hipdeviceprop_t
R 1376 5 11 hipfort_types regsperblock hipdeviceprop_t
R 1377 5 12 hipfort_types warpsize hipdeviceprop_t
R 1378 5 13 hipfort_types maxthreadsperblock hipdeviceprop_t
R 1379 5 14 hipfort_types maxthreadsdim hipdeviceprop_t
R 1380 5 15 hipfort_types maxgridsize hipdeviceprop_t
R 1381 5 16 hipfort_types clockrate hipdeviceprop_t
R 1382 5 17 hipfort_types memoryclockrate hipdeviceprop_t
R 1383 5 18 hipfort_types memorybuswidth hipdeviceprop_t
R 1384 5 19 hipfort_types totalconstmem hipdeviceprop_t
R 1385 5 20 hipfort_types major hipdeviceprop_t
R 1386 5 21 hipfort_types minor hipdeviceprop_t
R 1387 5 22 hipfort_types multiprocessorcount hipdeviceprop_t
R 1388 5 23 hipfort_types l2cachesize hipdeviceprop_t
R 1389 5 24 hipfort_types maxthreadspermultiprocessor hipdeviceprop_t
R 1390 5 25 hipfort_types computemode hipdeviceprop_t
R 1391 5 26 hipfort_types clockinstructionrate hipdeviceprop_t
R 1392 5 27 hipfort_types arch hipdeviceprop_t
R 1393 5 28 hipfort_types concurrentkernels hipdeviceprop_t
R 1394 5 29 hipfort_types pcidomainid hipdeviceprop_t
R 1395 5 30 hipfort_types pcibusid hipdeviceprop_t
R 1396 5 31 hipfort_types pcideviceid hipdeviceprop_t
R 1397 5 32 hipfort_types maxsharedmemorypermultiprocessor hipdeviceprop_t
R 1398 5 33 hipfort_types ismultigpuboard hipdeviceprop_t
R 1399 5 34 hipfort_types canmaphostmemory hipdeviceprop_t
R 1400 5 35 hipfort_types gcnarch hipdeviceprop_t
R 1401 5 36 hipfort_types gcnarchname hipdeviceprop_t
R 1402 5 37 hipfort_types integrated hipdeviceprop_t
R 1403 5 38 hipfort_types cooperativelaunch hipdeviceprop_t
R 1404 5 39 hipfort_types cooperativemultidevicelaunch hipdeviceprop_t
R 1405 5 40 hipfort_types maxtexture1dlinear hipdeviceprop_t
R 1406 5 41 hipfort_types maxtexture1d hipdeviceprop_t
R 1407 5 42 hipfort_types maxtexture2d hipdeviceprop_t
R 1408 5 43 hipfort_types maxtexture3d hipdeviceprop_t
R 1409 5 44 hipfort_types hdpmemflushcntl hipdeviceprop_t
R 1410 5 45 hipfort_types hdpregflushcntl hipdeviceprop_t
R 1411 5 46 hipfort_types mempitch hipdeviceprop_t
R 1412 5 47 hipfort_types texturealignment hipdeviceprop_t
R 1413 5 48 hipfort_types texturepitchalignment hipdeviceprop_t
R 1414 5 49 hipfort_types kernelexectimeoutenabled hipdeviceprop_t
R 1415 5 50 hipfort_types eccenabled hipdeviceprop_t
R 1416 5 51 hipfort_types tccdriver hipdeviceprop_t
R 1417 5 52 hipfort_types cooperativemultideviceunmatchedfunc hipdeviceprop_t
R 1418 5 53 hipfort_types cooperativemultideviceunmatchedgriddim hipdeviceprop_t
R 1419 5 54 hipfort_types cooperativemultideviceunmatchedblockdim hipdeviceprop_t
R 1420 5 55 hipfort_types cooperativemultideviceunmatchedsharedmem hipdeviceprop_t
R 1421 5 56 hipfort_types islargebar hipdeviceprop_t
R 1422 5 57 hipfort_types asicrevision hipdeviceprop_t
R 1423 5 58 hipfort_types managedmemory hipdeviceprop_t
R 1424 5 59 hipfort_types directmanagedmemaccessfromhost hipdeviceprop_t
R 1425 5 60 hipfort_types concurrentmanagedaccess hipdeviceprop_t
R 1426 5 61 hipfort_types pageablememoryaccess hipdeviceprop_t
R 1427 5 62 hipfort_types pageablememoryaccessuseshostpagetables hipdeviceprop_t
R 1428 5 63 hipfort_types gpufort_padding hipdeviceprop_t
A 12 2 0 0 0 6 673 0 0 0 12 0 0 0 0 0 0 0 0 0 0 0
A 68 1 0 0 0 62 733 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
A 71 1 0 0 0 71 735 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Z
J 127 1 1
V 68 62 7 0
S 0 62 0 0 0
A 0 6 0 0 1 2 0
J 128 1 1
V 71 71 7 0
S 0 71 0 0 0
A 0 6 0 0 1 2 0
T 1366 92 0 3 0 0
A 1367 6 0 0 1 3 1
A 1368 6 0 0 1 3 1
A 1369 6 0 0 1 3 0
Z
