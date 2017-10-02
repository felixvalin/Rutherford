#!/bin/bash

if [ $# -ge 1 ]; then
	mess=$1
	echo $mess
	branch=$2
else
	echo  -n "Commit message: "
	mess=$((read))
	echo -n "Branch: "
	branch=$((read))
fi


git add -A 

#git commit -a -m $mess 

git push origin $branch

