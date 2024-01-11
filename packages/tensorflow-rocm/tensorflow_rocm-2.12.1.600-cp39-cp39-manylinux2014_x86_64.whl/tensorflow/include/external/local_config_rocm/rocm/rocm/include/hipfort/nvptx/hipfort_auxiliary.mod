V34 :0x24 hipfort_auxiliary
106 /long_pathname_so_that_rpms_can_package_the_debug_info/src/extlibs/hipFORT/lib/hipfort/hipfort_auxiliary.f S668 0
12/12/2023  21:22:51
use iso_c_binding private
use hipfort_types private
enduse
D 60 20 12
D 62 26 697 8 696 7
D 71 26 700 8 699 7
D 92 26 1494 12 1493 3
D 101 26 1500 944 1499 7
S 668 24 0 0 0 9 1 0 5301 10005 0 A 0 0 0 0 B 0 1 0 0 0 0 0 0 0 0 0 0 38 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 hipfort_auxiliary
S 669 19 0 0 0 9 1 668 5319 4000 0 A 0 0 0 0 B 0 15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 1 0 0 0 0 0 668 0 0 0 0 hipgetdeviceproperties
O 669 1 670
S 670 14 5 0 0 6 1 668 5342 4 18000 A 1000000 0 0 0 B 0 17 0 0 0 0 0 2 2 0 0 675 0 0 0 0 0 0 0 0 0 17 0 668 0 0 674 0 hipgetdeviceproperties_
F 670 2 671 672
S 671 1 3 2 0 101 1 670 5366 2004 2000 A 0 0 0 0 B 0 17 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 prop
S 672 1 3 0 0 6 1 670 5371 2004 6000 A 0 0 0 0 B 0 17 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 deviceid
S 673 3 0 0 0 6 1 1 0 0 0 A 0 0 0 0 B 0 0 0 0 0 0 0 0 0 23 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6
S 674 3 0 0 0 60 0 1 0 0 0 A 0 0 0 0 B 0 0 0 0 0 0 0 0 5380 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 20 23 63 75 64 61 47 65 74 44 65 76 69 63 65 50 72 6f 70 65 72 74 69 65 73
S 675 1 3 0 0 6 1 670 5342 2004 1002000 A 0 0 0 0 B 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 hipgetdeviceproperties_
R 696 25 6 iso_c_binding c_ptr
R 697 5 7 iso_c_binding val c_ptr
R 699 25 9 iso_c_binding c_funptr
R 700 5 10 iso_c_binding val c_funptr
R 734 6 44 iso_c_binding c_null_ptr$ac
R 736 6 46 iso_c_binding c_null_funptr$ac
R 737 26 47 iso_c_binding ==
R 739 26 49 iso_c_binding !=
R 1493 25 1 hipfort_types dim3
R 1494 5 2 hipfort_types x dim3
R 1495 5 3 hipfort_types y dim3
R 1496 5 4 hipfort_types z dim3
R 1499 25 7 hipfort_types hipdeviceprop_t
R 1500 5 8 hipfort_types name hipdeviceprop_t
R 1501 5 9 hipfort_types uuid hipdeviceprop_t
R 1502 5 10 hipfort_types totalglobalmem hipdeviceprop_t
R 1503 5 11 hipfort_types sharedmemperblock hipdeviceprop_t
R 1504 5 12 hipfort_types regsperblock hipdeviceprop_t
R 1505 5 13 hipfort_types warpsize hipdeviceprop_t
R 1506 5 14 hipfort_types mempitch hipdeviceprop_t
R 1507 5 15 hipfort_types maxthreadsperblock hipdeviceprop_t
R 1508 5 16 hipfort_types maxthreadsdim hipdeviceprop_t
R 1509 5 17 hipfort_types maxgridsize hipdeviceprop_t
R 1510 5 18 hipfort_types clockrate hipdeviceprop_t
R 1511 5 19 hipfort_types totalconstmem hipdeviceprop_t
R 1512 5 20 hipfort_types major hipdeviceprop_t
R 1513 5 21 hipfort_types minor hipdeviceprop_t
R 1514 5 22 hipfort_types texturealignment hipdeviceprop_t
R 1515 5 23 hipfort_types texturepitchalignment hipdeviceprop_t
R 1516 5 24 hipfort_types deviceoverlap hipdeviceprop_t
R 1517 5 25 hipfort_types multiprocessorcount hipdeviceprop_t
R 1518 5 26 hipfort_types kernelexectimeoutenabled hipdeviceprop_t
R 1519 5 27 hipfort_types integrated hipdeviceprop_t
R 1520 5 28 hipfort_types canmaphostmemory hipdeviceprop_t
R 1521 5 29 hipfort_types computemode hipdeviceprop_t
R 1522 5 30 hipfort_types maxtexture1d hipdeviceprop_t
R 1523 5 31 hipfort_types maxtexture1dmipmap hipdeviceprop_t
R 1524 5 32 hipfort_types maxtexture1dlinear hipdeviceprop_t
R 1525 5 33 hipfort_types maxtexture2d hipdeviceprop_t
R 1526 5 34 hipfort_types maxtexture2dmipmap hipdeviceprop_t
R 1527 5 35 hipfort_types maxtexture2dlinear hipdeviceprop_t
R 1528 5 36 hipfort_types maxtexture2dgather hipdeviceprop_t
R 1529 5 37 hipfort_types maxtexture3d hipdeviceprop_t
R 1530 5 38 hipfort_types maxtexture3dalt hipdeviceprop_t
R 1531 5 39 hipfort_types maxtexturecubemap hipdeviceprop_t
R 1532 5 40 hipfort_types maxtexture1dlayered hipdeviceprop_t
R 1533 5 41 hipfort_types maxtexture2dlayered hipdeviceprop_t
R 1534 5 42 hipfort_types maxtexturecubemaplayered hipdeviceprop_t
R 1535 5 43 hipfort_types maxsurface1d hipdeviceprop_t
R 1536 5 44 hipfort_types maxsurface2d hipdeviceprop_t
R 1537 5 45 hipfort_types maxsurface3d hipdeviceprop_t
R 1538 5 46 hipfort_types maxsurface1dlayered hipdeviceprop_t
R 1539 5 47 hipfort_types maxsurface2dlayered hipdeviceprop_t
R 1540 5 48 hipfort_types maxsurfacecubemap hipdeviceprop_t
R 1541 5 49 hipfort_types maxsurfacecubemaplayered hipdeviceprop_t
R 1542 5 50 hipfort_types surfacealignment hipdeviceprop_t
R 1543 5 51 hipfort_types concurrentkernels hipdeviceprop_t
R 1544 5 52 hipfort_types eccenabled hipdeviceprop_t
R 1545 5 53 hipfort_types pcibusid hipdeviceprop_t
R 1546 5 54 hipfort_types pcideviceid hipdeviceprop_t
R 1547 5 55 hipfort_types pcidomainid hipdeviceprop_t
R 1548 5 56 hipfort_types tccdriver hipdeviceprop_t
R 1549 5 57 hipfort_types asyncenginecount hipdeviceprop_t
R 1550 5 58 hipfort_types unifiedaddressing hipdeviceprop_t
R 1551 5 59 hipfort_types memoryclockrate hipdeviceprop_t
R 1552 5 60 hipfort_types memorybuswidth hipdeviceprop_t
R 1553 5 61 hipfort_types l2cachesize hipdeviceprop_t
R 1554 5 62 hipfort_types persistingl2cachemaxsize hipdeviceprop_t
R 1555 5 63 hipfort_types maxthreadspermultiprocessor hipdeviceprop_t
R 1556 5 64 hipfort_types streamprioritiessupported hipdeviceprop_t
R 1557 5 65 hipfort_types globall1cachesupported hipdeviceprop_t
R 1558 5 66 hipfort_types locall1cachesupported hipdeviceprop_t
R 1559 5 67 hipfort_types sharedmempermultiprocessor hipdeviceprop_t
R 1560 5 68 hipfort_types regspermultiprocessor hipdeviceprop_t
R 1561 5 69 hipfort_types managedmemory hipdeviceprop_t
R 1562 5 70 hipfort_types ismultigpuboard hipdeviceprop_t
R 1563 5 71 hipfort_types multigpuboardgroupid hipdeviceprop_t
R 1564 5 72 hipfort_types singletodoubleprecisionperfratio hipdeviceprop_t
R 1565 5 73 hipfort_types pageablememoryaccess hipdeviceprop_t
R 1566 5 74 hipfort_types concurrentmanagedaccess hipdeviceprop_t
R 1567 5 75 hipfort_types computepreemptionsupported hipdeviceprop_t
R 1568 5 76 hipfort_types canusehostpointerforregisteredmem hipdeviceprop_t
R 1569 5 77 hipfort_types cooperativelaunch hipdeviceprop_t
R 1570 5 78 hipfort_types cooperativemultidevicelaunch hipdeviceprop_t
R 1571 5 79 hipfort_types pageablememoryaccessuseshostpagetables hipdeviceprop_t
R 1572 5 80 hipfort_types directmanagedmemaccessfromhost hipdeviceprop_t
R 1573 5 81 hipfort_types accesspolicymaxwindowsize hipdeviceprop_t
R 1574 5 82 hipfort_types gpufort_padding hipdeviceprop_t
A 12 2 0 0 0 6 673 0 0 0 12 0 0 0 0 0 0 0 0 0 0 0
A 68 1 0 0 0 62 734 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
A 71 1 0 0 0 71 736 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Z
J 127 1 1
V 68 62 7 0
S 0 62 0 0 0
A 0 6 0 0 1 2 0
J 128 1 1
V 71 71 7 0
S 0 71 0 0 0
A 0 6 0 0 1 2 0
T 1493 92 0 3 0 0
A 1494 6 0 0 1 3 1
A 1495 6 0 0 1 3 1
A 1496 6 0 0 1 3 0
Z
