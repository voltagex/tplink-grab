
There are non tar files in the old download I did, the current download hasn't finished at the time of writing.

TODO: extract zip, rar and nested tar/gz files.

```sh
zpool create pool -O dedup=on /dev/sda5
zfs set compression=zstd pool
zfs create pool/data
zfs set mountpoint=/data pool/data
for t in /tmp/share/Data/Compressed/TPLink/*.tar*; do ( echo $t;tar --one-top-level -axf "$t" ) &>> /tmp/share/Data/Compressed/TPLink/extract.log; done
```


TP-Link removed the following files between 2020 and 2022 (probably more, but I only did two crawls)

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
