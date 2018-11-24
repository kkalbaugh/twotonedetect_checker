#!/bin/bash
{
	echo "--- Checking for root privileges..."
	if [ "`whoami`" != "root" ]; then
	echo Error: This script requires root access
	exit 1
	fi
	apt install python3-dev libpython3-dev
	apt-get install python3-pip
		pip install --upgrade pip
		python3 -m pip install smtplib
	python3 -m pip install boto3
	if [ ! -d /usr/share/ttd_checker ];
	then
		echo "Creating ttd_checker directory";
		mkdir /usr/share/ttd_checker
		echo "Copying files over";
		rsync -v *.py /usr/share/ttd_checker/
	else
		echo "Copying files over";
		#cp -R *.py!(config.py) /usr/share/ttd_checker/
		rsync -v --exclude='config.py' *.py /usr/share/ttd_checker/
	fi		
	if [ ! -d /var/local/ttd_checker/ ];
	then
		echo "Creating lastsent directory";
		mkdir /var/local/ttd_checker/
		touch /var/local/ttd_checker/lastsent.txt
		chmod 777 /var/local/ttd_checker/lastsent.txt
	fi
		
	chown root:root -R /usr/share/ttd_checker
	chmod 755 -R /usr/share/ttd_checker

	echo '*/30 * * * * root /usr/bin/python3 /usr/share/ttd_checker/ttd_checker.py &' > /etc/cron.d/ttd_checker
	echo "Added ttd_checker.py to /etc/cron.d/ttd_checker"
}
