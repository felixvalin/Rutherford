#!/bin/bash

if [ $# = 0 ]; then
	mess = $1
else
	echo  -n "Commit message: "
	mess = $((read))
fi


git add -A && git commit -a -m mess && git push origin master
