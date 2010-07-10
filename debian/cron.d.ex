#
# Regular cron jobs for the lamp-icon package
#
0 4	* * *	root	[ -x /usr/bin/lamp-icon_maintenance ] && /usr/bin/lamp-icon_maintenance
