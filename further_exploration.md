
There are non tar files in the old download I did, the current download hasn't finished at the time of writing.

TODO: extract zip, rar and nested tar/gz files.

```sh
zpool create pool -O dedup=on /dev/sda5
zfs set compression=zstd pool
zfs create pool/data
zfs set mountpoint=/data pool/data
for t in /tmp/share/Data/Compressed/TPLink/*.tar*; do ( echo $t;tar --one-top-level -axf "$t" ) &>> /tmp/share/Data/Compressed/TPLink/extract.log; done
```


Realised that I accidentally excluded not tar files from the latest download.
