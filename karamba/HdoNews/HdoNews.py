#Written by NightMan (nobodysplace@web.de)
#Heise Newsreader


#this import statement allows access to the karamba functions
import karamba
import string
import urllib2

# Theme desgin 
theme_width = 500
theme_height = 200
line_height=21
lines = 10
r = 255
g = 255
b = 255


# Menuconfig Option
browser_pid = 0

# Heise Urls
heise_url = ["http://www.heise.de/newsticker/heise.rdf", "http://www.heise.de/mobil/newsticker/heise.rdf", "http://www.heise.de/security/news/news.rdf"]

# Don't touch or be careful
update = 1
item = []
link = []
item_cnt = 0
itempointer = []
scroll = 0
urlpointer = 0
fill = []
clickScrollUp = 0
clickScrollDown = 0
browserCommand = ""

# Get Title
def getTitle():
	global heise
	
	cnt_start = heise.find("<title>")+7
	cnt_end = heise.find("</title>")
	title = heise[cnt_start:cnt_end]
	heise = heise[cnt_end:]
	return title


# Get Description
def getDescription():
	global heise
	
	cnt_start = heise.find("<description>")+13
	cnt_end = heise.find("</description>")
	description = heise[cnt_start:cnt_end]
	heise = heise[cnt_end:]
	return description

# Get Content
def getItem():
	global heise, item, link, item_cnt
	
	jump = 1
	item_cnt = 0
	while jump > 0:
		# find item
		cnt_start = heise.find("<title>")+7
		cnt_end = heise.find("</title>")
	
		# Set Content 
		item.insert(item_cnt, heise[cnt_start:cnt_end])

		# find Link
		cnt_start = heise.find("<link>")+6
		cnt_end = heise.find("</link>")

		#Set Link
		link.insert(item_cnt, heise[cnt_start:cnt_end])
		
		# Cut String
		cnt_end = heise.find("</item>")+7
		heise = heise[cnt_end:]
		
		jump = heise.find("<title>")
		item_cnt = item_cnt + 1
		


## Execute Command (lynx) for Heise
def getHeise(url):
	global heise

	filehandle = urllib2.urlopen(url)
	heise = filehandle.read()
	


def setStyle(widget, text, shadow, size):
	karamba.changeTextSize(widget, text, size)
	karamba.changeTextFont(widget, text, "arialbd")
	karamba.changeTextShadow(widget, text, shadow)


def fillContent(widget, what):
	global itempointer, scroll
	
	if what == "up":
		scroll = scroll - 12
		if scroll < 1:
			scroll = 0
	elif what == "down":
		scroll = scroll + 3
		max_start = item_cnt - lines
		if scroll > max_start:
			scroll = max_start
	elif what == "refresh":
		getHeise(heise_url[urlpointer])
		getDescription()
		getItem()
		scroll = 0
	
	z = 0 
	y_pos = 23
	print "\n#### Fill Content ####"
	while scroll < item_cnt and z < lines: 
		news = item[scroll]
		link_to = link[scroll]
		print item[scroll]

		content = karamba.changeText(widget, itempointer[z], news[:49]+' ...')			
		setStyle(widget, content, 1, 17)
		karamba.changeTextColor(widget, content, r,g,b)

		cmd = browserCommand.split()
		cmd_link = cmd[0] + " "+link_to
		karamba.attachClickArea(widget, content, cmd_link)
		y_pos = y_pos + 15
		scroll = scroll + 1
		z = z + 1
	print "#### End Content ####\n"

	if scroll == 10:
		scroll = 0


def createMenu(widget):
	global fill

	## Set Title Heise ## 
	getTitle()

	#first = karamba.createText(widget, 14, 1, 50, line_height, "Heise:")
	#setStyle(widget, first, 7, 15)
	#karamba.changeTextColor(widget, first, r,g,b)
	
	fill.insert(0, karamba.createText(widget, 90, 1, 50, line_height, "Online"))
	setStyle(widget, fill[0], 7, 15)
	karamba.changeTextColor(widget, fill[0], r,g,b)
	karamba.attachClickArea(widget, fill[0], "")
	
	## Set Title Mobile 
	fill.insert(1, karamba.createText(widget, 175, 1, 50, line_height, "Mobil"))
	setStyle(widget, fill[1], 7, 15)
	karamba.changeTextColor(widget, fill[1], r,g,b)
	karamba.attachClickArea(widget, fill[1], "")
	
	## Set Title Security 
	fill.insert(2, karamba.createText(widget, 255, 1, 60, line_height, "Security"))
	setStyle(widget, fill[2], 7, 15)
	karamba.changeTextColor(widget, fill[2], r,g,b)
	karamba.attachClickArea(widget, fill[2], "")
	
	## Set Description
	getDescription()
	#fill = karamba.createText(widget, 5, 1, 170, line_height, description)
	#setStyle(widget, fill, 7, 15)
	#karamba.changeTextColor(widget, fill, 255,255,255)


#this is called when you widget is initialized
def initWidget(widget):
	global itempointer, diff, clickScrollUp, clickScrollDown, update, browserCommand
	
	getHeise(heise_url[urlpointer])
	createMenu(widget)

	y_pos = 23
	z = 0 
	while z < lines:
   		itempointer.insert(z ,karamba.createText(widget, 14, y_pos, theme_width-18, line_height, ""))
		setStyle(widget, itempointer[z], 1, 17)
		karamba.changeTextColor(widget, itempointer[z], r,g,b)
		y_pos = y_pos + 15
		z = z + 1
	
	karamba.changeTextColor(widget, fill[0], 54,227,123)
#	karamba.changeTextColor(widget, fill[0], 255,255,255)
	# Menuoption "browser"
	karamba.addMenuConfigOption(widget, "browser", "Change your browser")
	browserCommand = karamba.readConfigEntry(widget, "browser") or "konqueror"
	# Up
	clickScrollUp = karamba.createImage(widget, 0, 0, "up.png")
	karamba.moveImage(widget, clickScrollUp, 50, 2)
	karamba.attachClickArea(widget, clickScrollUp, "")

	#Down
	clickScrollDown = karamba.createImage(widget, 0, 0, "down.png")
	karamba.moveImage(widget, clickScrollDown, 22, 3)
	karamba.attachClickArea(widget, clickScrollDown, "")
	
	fillContent(widget, "refresh")
	update = 0
	widgetUpdated(widget)
	
	
#this is called everytime your widget is updated
#the update inverval is specified in the .theme file
def widgetUpdated(widget):
	global update

	if update == 1:
		print "Update Theme"
		fillContent(widget, "refresh")

	update = 1

	
#This gets called everytime our widget is clicked.
#Notes:
#  widget = reference to our widget
#  x = x position (relative to our widget)
#  y = y position (relative to our widget)
#  botton = button clicked:
#                    1 = Left Mouse Button
#                    2 = Middle Mouse Button
#                    3 = Right Mouse Button, but this will never happen
#                        because the right mouse button brings up the
#                        Karamba menu.
#                    4,5 = Scroll wheel up and down
def widgetClicked(widget, x, y, button):
	pass
		

#This gets called everytime our widget is clicked.
#Notes
#  widget = reference to our widget
#  x = x position (relative to our widget)
#  y = y position (relative to our widget)
#  botton = button being held:
#                    0 = No Mouse Button
#                    1 = Left Mouse Button
#                    2 = Middle Mouse Button
#                    3 = Right Mouse Button, but this will never happen
#                        because the right mouse button brings up the
#                        Karamba menu.
#Warning:  Don't do anything too intensive here
#You don't want to run some complex piece of code everytime the mouse moves
def widgetMouseMoved(widget, x, y, button):
	pass

#This gets called when an item is clicked in a popup menu you have created.
#  menu = a reference to the menu
#  id = the number of the item that was clicked.
def menuItemClicked(widget, menu, id):
    pass

#This gets called when an item is clicked in the theme CONFIGURATION menu,
#not the popup menus that you create.
#  key = the reference to the configuration key that was changed
#  value = the new value (true or false) that was selected
def menuOptionChanged(widget, key, value):
	global browser_pid

	if key == "browser":
		karamba.setMenuConfigOption(widget, "browser", 0)
		command = ["kdialog", "--title", "Enter the path to your favorite browser", "--inputbox", "Path to browser", "/usr/bin/mozilla"]
		browser_pid = karamba.executeInteractive(widget, command)



#This gets called when a meter (image, text, etc) is clicked.
# NOTE you must use attachClickArea() to make a meter
# clickable.  
#  widget = reference to your theme
#  meter = the meter clicked
#  button = the button clicked (see widgetClicked for button numbers)
def meterClicked(widget, meter, button):
	global urlpointer, update
	
	drin = 0
	if meter == fill[0] and button == 1:
		drin = 1
		urlpointer = 0
	elif meter == fill[1] and button == 1:
		urlpointer = 1
		drin = 1
	elif meter == fill[2] and button == 1:
		urlpointer = 2
		drin = 1
	elif meter == clickScrollUp:
		print "Scroll Up"
		update = 0 
		fillContent(widget,"up")
	elif meter == clickScrollDown:
		print "Scroll Down"
		update = 0 
		fillContent(widget,"down")

	if drin == 1:
		print "Click Menu"
		createMenu(widget)		
		karamba.changeTextColor(widget, fill[urlpointer], 54,227,123)
#		karamba.changeTextColor(widget, fill[urlpointer], 255,255,255)
		update = 0 
		fillContent(widget, "refresh")


#This gets called when a command you have executed with executeInteractive() outputs something
#to stdout.  This way you can get the output of for example kdialog without freezing up the widget
#waiting for kdialog to end.
#  widget = reference to your theme
#  pid = process number of the program outputting (use this if you execute more than out process)
#  output = the text the program outputted to stdout
def commandOutput(widget, pid, output):
	global browsercommand
	if pid == browser_pid:
		karamba.writeConfigEntry(widget, "browser", output)
		browserCommand = output
	pass


#This gets called when an item is dropped on this widget.
# NOTE you have to call acceptDrops() before your widget will accept drops.
#  widget = reference to your theme
#  dropText = the text of the dropped item (probably a URL to it's location in KDE)
def itemDropped(widget, dropText):
    pass


#This gets called when a new program is LOADING in KDE.  When it is done
#loading, startupRemoved() is called, followed by taskAdded().
#  widget = reference to your widget
#  task = A refence to the task that is starting.  
def startupAdded(widget, startup):
    pass

#This gets called when a new program is done LOADING in KDE.
#  widget = reference to your widget
#  task = A refence to the task that just finished loading.  
def startupRemoved(widget, startup):
    pass

#This is called every time a new task (program) is started in KDE.
#  widget = reference to your widget
#  task = A refence to the new task.  Call getTaskInfo() with this reference
#         to get the name, etc of this new task.
def taskAdded(widget, task):
    pass

#This is called everytime a task (program) is closed in KDE.
#  widget = reference to your widget
#  task = A refence to the task.  
def taskRemoved(widget, task):
    pass

#This is called everytime a different task gains focus (IE, the user clicks
#on a different window).  
#  widget = reference to your widget
#  task = A refence to the task.  Call getTaskInfo() with this reference
#         to get the name, etc of this new task.
def activeTaskChanged(widget, task):
    pass

# This will be printed when the widget loads.
print "Loaded my python extension!"

