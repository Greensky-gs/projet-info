#!/bin/bash

RES=$(pyassembler --help >/dev/null 2>/dev/null)
VALID=$(( $? == 0 ))

if [[  $VALID == 0 ]]; then
	echo "PyAssembler not found. Maybe try to install as README says"
	exit 1
fi

opts_flags=

if [[ $1 == "--prod" ]]; then
	opts_flags=--no-comments
fi

pyassembler src -v -o build/main.py --last-file main.py --max-newlines 2  --start-of-file "Start Of File " --end-of-file "End Of File " --fullpaths $opts_flags

