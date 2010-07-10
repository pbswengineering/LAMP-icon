#! /usr/bin/python2


# Handy tray icon to manage the LAMP services (Apache + MySQL) on 
# Ubuntu 10.04 with a single mouse click.
#
# by Paolo Bernardi <villa.lobos@tiscali.it>


import gtk
import os
import subprocess
import shlex
import sys
	
	
def analyze_status():
	"""Analyzes the LAMP services status.
	Returns a dictionary with the following informations:
	- "is_running": True if every LAMP service is up, False otherwise;
	- "icon": a confirmation icon if every LAMP service is running,
	          a warning icon if some LAMP service is down,
		  an error icon if every LAMP service is down;
	- "text": a text caption describing the LAMP services status.
	"""
	
	pa = subprocess.Popen(shlex.split("service apache2 status"), shell=False, stdout=subprocess.PIPE)
	apache2 = pa.stdout.read().find(' NOT ') == -1
	pm = subprocess.Popen(shlex.split("service mysql status"), shell=False, stdout=subprocess.PIPE)
	mysql = pm.stdout.read().find('start') != -1
	
	if apache2:
		text = "Apache is running\n"
	else:
		text = "Apache is NOT running\n"
	if mysql:
		text += "MySQL is running"
	else:
		text += "MySQL is NOT running"
		
	if apache2 and mysql:
		return {"is_running": True, "icon": gtk.STOCK_YES, "text": text}
	elif apache2 or mysql:
		return {"is_running": False, "icon": gtk.STOCK_DIALOG_WARNING, "text": text}
	else:
		return {"is_running": False, "icon": gtk.STOCK_STOP, "text": text}


def update_icon(status):
	"""Updates the tray icon and its popup text depending on the LAMP
	services status.
	The parameter status is the dictionary returned from analyze_status.
	"""
	
	global status_icon
	status_icon.set_from_stock(status["icon"])
	status_icon.set_tooltip_text(status["text"])


def status_icon_clicked(widget, event):
	"""Acts upon a user click on the tray icon, alternating start and stop
	of every LAMP service.
	"""
	
	if event.button == 1:
		global toggled
		status = analyze_status()
		s = toggled and "stop" or "start"
		# Apparently, service apache2 start/stop doesn't work if not run in a terminal
		# apache2ctl works anyway, so I used it
		subprocess.call(shlex.split("gksudo apache2ctl %s" % s))
		subprocess.call(shlex.split("gksudo service mysql %s" % s))
		update_icon(analyze_status())
		toggled = not toggled


def package_installed(package):
	"""Returns True if package is installed, False otherwise."""
	
	pa = subprocess.Popen(shlex.split("dpkg -l " + package), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return pa.stderr.read().find("No packages found matching " + package) == -1


def check_environment():
	"""Checks if the environment is good (LAMP services are there?
	Python and GTK versions are correct?).
	If there's something wrong returns a message about it, otherwise
	returns an empty string.
	"""
	
	messages = []
	
	if sys.version_info[0] != 2 or sys.version_info[1] < 6:
		messages.append("Python 2.6 or greater is needed (but not Python 3).")
		
	if gtk.gtk_version[0] < 2 or gtk.gtk_version[1] < 10:
		messages.append("GTK 2.10 or greater is needed.")
		
	if not package_installed("apache2"):
		messages.append("You need to install apache2")
		
	if not package_installed("mysql-server"):
		messages.append("You need to install mysql-server")
		
	return "\n".join(messages)
	
	
if __name__ == "__main__":
	errors = check_environment()
	if not errors:
		global status_icon, toggled
		status_icon = gtk.StatusIcon()
		status = analyze_status()
		toggled = status["is_running"]
		update_icon(status)
		status_icon.connect("button-press-event", status_icon_clicked)
		gtk.main()
	else:
		m = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, 
					buttons=gtk.BUTTONS_CLOSE,
					message_format=errors)
		m.set_title("Something's wrong...")
		m.run()
		m.destroy()