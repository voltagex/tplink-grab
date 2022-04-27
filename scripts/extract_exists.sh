#!/bin/bash
set -u

IFS=$(echo -en "\n\b")
DATE=`date +%s`
for t in $1/*.tar*; do 
( 
filename=$(basename -- "$t")
dirname="${filename%%.tar*}"
if [ ! -d "$dirname" ]
then
	echo $t
	tar --one-top-level -axf "$t"
fi

) &>> extract-$DATE.log
done;

for t in $1/*.tgz; do 
( 
filename=$(basename -- "$t")
dirname="${filename%%.tgz}"
if [ ! -d "$dirname" ]
then
	echo $t
	tar --one-top-level -axf "$t"
fi


) &>> extract-$DATE.log
done;


for r in $1/*.rar; do 
( 
filename=$(basename -- "$r")
dirname="${filename%%.rar}"
if [ ! -d "$dirname" ]
then
	echo $r
	unrar x -op$dirname $r
fi

) &>> extract-$DATE.log
done;

echo last
for z in $1/*.zip; do 
( 
filename=$(basename -- "$z")
dirname="${filename%%.zip}"
if [ ! -d "$dirname" ]
then
	echo $z
	unzip $z -d $dirname
fi

) &>> extract-$DATE.log
done;
