# ***********************************
# *
# *	Calendar for Superkaramba
# *	(C) by Thomas Gollenia
# *	email: baraquda@gmx.com
# *	License: BSD
# *
# *	the out-commented print commands are for debugging only!
# ************************************


import karamba
import ckalendar
import os
import locale
import string
import datetime
from threading import *

# Create a new calendar Object
global calendar
calendar = ckalendar.cKalendar()


def initWidget(widget):
	
	
	# add a menu entry to select language
	karamba.addMenuConfigOption(widget, "ac_locale", "Select your country")
	karamba.setMenuConfigOption(widget, "ac_locale", 0)
	
	# set the language
	locale.setlocale(locale.LC_ALL, getLocale(widget))
	
	
	# Generate calendar
	calendar.printTop(widget, 0)
#	calendar.showWeekImage(widget, 0)
	calendar.showDayMarker(widget, 0)
	calendar.printDayCaptions(widget, 0)
	calendar.printCalendar(widget, 0)
	calendar.colorizeDay(widget, calendar.thisDay, 255, 255, 255)
	 #calendar.colorizeWeek(widget, 0, 0, 100)


def widgetUpdated(widget):
	calendar.updateClass()
	locale.setlocale(locale.LC_ALL, getLocale(widget))
	calendar.printTop(widget, 1)
#	calendar.showWeekImage(widget, 1)
	calendar.showDayMarker(widget, 1)
	calendar.printDayCaptions(widget, 1)
	calendar.printCalendar(widget, 1)
	calendar.colorizeDay(widget, calendar.thisDay, 255, 255, 255)


def getLocale(widget):
	GetLocale = karamba.readConfigEntry(widget, "locale") # have you set any language?
	if GetLocale == None:
		# no language found, using english
		# print "No locale-setting was found. Using English en_US"
		karamba.writeConfigEntry(widget, "locale", "en_US")
		SetLocale = "en_US.ISO8859-1"	
	else:
		# language found! using it
		# print "Locale-setting " + SetLocale + " was found!"
		SetLocale = GetLocale + ".ISO8859-1"
	return SetLocale
	# language is stored in SetLocale now. let's use it:



def menuOptionChanged(widget, key, value):
	global localePid
	localeSelection = ["kdialog", "--title", "Country Selector", "--radiolist", "Please select your language:", "en_US", "English", "off", "de_DE", "German", "off", "es_ES", "Spanish", "off", "nl_BE", "Dutch", "off", "fr_FR", "French", "off", "fi_FI", "Finnish", "off", "it_IT", "Italian", "off"]
	if (key == "ac_locale"):
		karamba.setMenuConfigOption(widget, "ac_locale", 0)
		localePid = karamba.executeInteractive(widget, localeSelection)


def commandOutput(widget, pid, output):
	if pid == localePid:
		localeString = output.replace('\n','')
		print "New language " + localeString + " was selected!"
		karamba.writeConfigEntry(widget, "locale", localeString)
		getLocale(widget)
		

	