#!/bin/bash

mypy=$(python -c 'import sys; print("%d.%d" % (sys.version_info.major, sys.version_info.minor))')
directory=$(readlink -f $0)

install_requests() {
	pip > /dev/null 2>&1
	if [[ $? -eq 0 ]]; then
		sudo pip install requests
	else
		easy_install > /dev/null 2>&1
		if [[ $? -eq 1 ]]; then
			sudo easy_install requests
		else
			echo "Unable to install requests. Please install requests with pip or easy_install and try again."
			exit
		fi
	fi
}

if [[ $mypy < '2.6' ]]; then
	echo "Too old for this library! This requires Python 2.6 or above."
	exit
elif [[ $mypy > '2.9' ]]; then
	#statements
	echo "This supports Python 3! Making the necessary changes (xrange -> range, etc)...\n"
	sed -i 's/xrange/range/g' $directory/*.py
fi
echo "Checking for presence of required Requests module..."
python -c 'import requests' > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
	install_requests
fi

