
Misnamed and non .tar.gz files did cause me some issues.

```sh
zpool create pool -O dedup=on /dev/sda5
zfs set compression=zstd pool
zfs create pool/data
zfs set mountpoint=/data pool/data
for t in /tmp/share/Data/Compressed/TPLink/*.tar*; do ( echo $t;tar --one-top-level -axf "$t" ) &>> /tmp/share/Data/Compressed/TPLink/extract.log; done
```


TP-Link removed the following files between 2020 and 2022 (probably more, but I only did two crawls)

```diff
-EAP225-Outdoorv1_GPL.tar.gz
-EAP225V3_GPL.tar.gz
-EAP245V3_GPL.tar.bz2
-GPL-M9Plus.tar.bz2
-GPL_ArcherC20V4.tar.gz
-GPL_ArcherVR500vV1.tar.gz
-GPL_M5_V3.tar.gz
-IPCAM_GM812x_GPL.rar
-TL-WR802NV4_GPL.tar.gz
-ax3000v1_GPL.tar.gz
-ax50v1_GPL.tar.gz
-eap225-wallv2_GPL.tar.gz
-gpl_oc200.tar.bz2
-t1600g-28ts_gpl.tar.gz
-wpa8630pv2.1_au_GPL.tar.gz
```


Files that will need special handling (i.e not tar, or better wildcards) to extract them:

```
ls -1 | grep -vE '.tar|.txt|.log'
11N_GPL.tgz
ArcherC7v2_un_gpl.zip
Archer_MR200V5_GPL.rar
Archer_MR400V4_GPL.rar
CPE610(UN)1.0_GPL.rar
EAP Controller_V2.5_GPL.zip
EAP320_1.0_gpl_code.zip
EAP330_1.0_gpl_code.zip
GPL TD_W8970V3.gz
GPL-M5.zip
GPL_Archer_VR1210v.tgz
GPL_CODE_C50V4.2_RU.zip
GPL_CODE_C50V4_RU.zip
GPL_VR400V2.tgz
NC200 1.0 GPL.rar
NC220 1.0 GPL.rar
NC450_1.0_GPL.rar
RE200v2_GPL.rar
RE450_V2_GPL.zip
SmartPlug_GPL.tgz
TL-MR6400(APAC)5.0_GPL.rar
TL-MR6400V5_GPL_ALL.rar
TL-WA830RE_V3.bz2
TL-WA850RE(EU)_V5_GPL.zip
TL-WA855RE(EU)_V3_GPL.zip
TL-WA850RE(EU)_V5_GPL.zip
TL-WA855RE(EU)_V3_GPL.zip
TL-WA860RE(EU)_V5_GPL.zip
TL-WA865REv5_GPL.rar
TL-WPA4530_KIT_V2_GPL_Code.zip
TL-WPA7510 KIT V1.0_GPL.rar
TL-WPA8630_V1.0_GPL_CODE.rar
TL-WPA9610_KIT_V1.0_GPL.gz
TL-WR740Nv6.rar
TL-WR741ND_WR740N_V3.rar
TL-WR840N_V6.20.GPL.gz
TL-WR840v2_GPL.rar
TL-WR841nv11_GPL.rar
TL-WR842ND(RU) 2.0_GPL.rar
TL-WR849N_V6.20_GPL.gz
TL_WR1043v3_GPL.rar
TL_WR802NV1_GPL.rar
TL_WR841V10_GPL.rar
TouchP5v1_GPL_Source.zip
WA901ndv4_en_GPL.rar
WPA4230-GPL.tgz
branch_hornet_linux.rar
re350v1-gpl-code.zip
re450v3_gplcode.rar
re455v1_opensource.rar
re500xv1_gplcode.zip
re505xv1_gplcode.zip
re605xv1_gplcode.zip

```

and

```
AX11000_GPL_20190724.tar.gz:                      bzip2 compressed data, block size = 900k
Archer_C7_1.0.tar.gz:                             bzip2 compressed data, block size = 900k
GPL_C8v4_eu_us_20170417.tar.gz:                   bzip2 compressed data, block size = 900k
GPL_C9v4_US_20170110.tar.gz:                      bzip2 compressed data, block size = 900k
GPL_C9v5_EU_20170110.tar.gz:                      bzip2 compressed data, block size = 900k
GPL_TL-WR941NDV6.tar.gz:                          RAR archive data, v4, os: Win32
GPL_e4r.tar.gz:                                   POSIX tar archive (GNU)
NC250V1.tar.gz:                                   bzip2 compressed data, block size = 900k
TL-WPA9610_KIT_V1.0_GPL.gz:                       POSIX tar archive (GNU)
TL-WR1042ND_GPL_Code.tar.gz:                      bzip2 compressed data, block size = 900k
TL-WR843ND(UN)1.0_GPL.tar.gz:                     bzip2 compressed data, block size = 900k
eap225-odv3-gpl.tar.gz:                           POSIX tar archive (GNU)
re600xv2_gplcod.tar.gz:                           POSIX tar archive (GNU)
855rev1_eu_gpl_code.tar.bz2:                      gzip compressed data
8968V2_OpenSource.tar.bz2:                        gzip compressed data
TL-ER6020(UN)2.0_GPL.tar.bz2:                     gzip compressed data
TL-R480T-plus(UN)9.0_GPL.tar.bz2:                 gzip compressed data
TL-R600VPN(UN)4.0-GPL-new.tar.bz2:                gzip compressed data
WPA8730_GPL_CODE(20160616).tar.bz2:               gzip compressed data
eap_gpl_code.tar.bz2:                             gzip compressed data
RE450_V2_GPL.zip:                                 bzip2 compressed data, block size = 900k
```

manually collated with 

```
file *.gz | grep -v gzip
file *.tgz | grep -v gzip
file *.bz2 | grep -v bzip | cut -d ',' -f1
file *.rar | grep -v RAR
file *.zip | grep -v Zip
```

Future ideas:
Rename all files to hashes, symlink to hash or similar to remove duplicates

`( find . -type f -print0 | xargs -0 -P16 sha256sum > ../sha256sums ) &>> ../log-sha256sums`
