#               +++ crystalclock +++
#   this is my first try to create a clock for superkaramba
#   code by georg veit
#   license for source code and artwork: public domain
#   !!! fast image scaling MUST be turned off or misteriuos things happen !!!

import karamba
import time
import math

class Hand:
	def __init__(self,widget,handimage,shadowimage,scale,pivot_x,pivot_y,center_x,center_y,shadowlevel):
		self.imgshadow=karamba.createImage(widget,0,0,shadowimage)
		self.imghand=karamba.createImage(widget,0,0,handimage)
		hw=karamba.getImageWidth(widget,self.imghand)
		hh=karamba.getImageHeight(widget,self.imghand)
		r1=math.sqrt((pivot_x*pivot_x)+(pivot_y*pivot_y))
		r4=r1
		a1=math.pi-math.asin(pivot_y/r1)
		a4=2.0*math.pi-a1
		r2=math.sqrt((pivot_y*pivot_y)+((hw-pivot_x)*(hw-pivot_x)))
		r3=r2
		a2=math.asin(pivot_y/r2)
		a3=-a2
		self.a1=a1
		self.a2=a2
		self.a3=a3
		self.a4=a4
		self.r1=r1*scale
		self.r2=r2*scale
		self.r3=r3*scale
		self.r4=r4*scale
		self.center_x=center_x
		self.center_y=center_y
		self.shadowlevel=shadowlevel
		self.prev=0.0	#prevents rotating etc. if not required
		
	def draw(self,widget,angle):
		if (self.prev==angle):
			return
		self.prev=angle
		karamba.rotateImage(widget,self.imgshadow,angle)
		karamba.rotateImage(widget,self.imghand,angle)
		a=angle/180.0*math.pi
		x1=self.center_x+self.r1*math.cos(a+self.a1)
		y1=self.center_y+self.r1*math.sin(a+self.a1)
		x2=self.center_x+self.r2*math.cos(a+self.a2)
		y2=self.center_y+self.r2*math.sin(a+self.a2)
		x3=self.center_x+self.r3*math.cos(a+self.a3)
		y3=self.center_y+self.r3*math.sin(a+self.a3)
		x4=self.center_x+self.r4*math.cos(a+self.a4)
		y4=self.center_y+self.r4*math.sin(a+self.a4)
		xl=x1
		if (x2<xl):
			xl=x2
		if (x3<xl):
			xl=x3
		if (x4<xl):
			xl=x4
		yl=y1
		if (y2<yl):
			yl=y2
		if (y3<yl):
			yl=y3
		if (y4<yl):
			yl=y4
		xm=x1
		if (x2>xm):
			xm=x2
		if (x3>xm):
			xm=x3
		if (x4>xm):
			xm=x4
		ym=y1
		if (y2>ym):
			ym=y2
		if (y3>ym):
			ym=y3
		if (y4>ym):
			ym=y4
		karamba.resizeImage(widget,self.imgshadow,int(xm-xl),int(ym-yl))
		karamba.moveImage(widget,self.imgshadow,int(xl),int(yl)+self.shadowlevel)
		karamba.resizeImage(widget,self.imghand,int(xm-xl),int(ym-yl))
		karamba.moveImage(widget,self.imghand,int(xl),int(yl))
		

def initWidget(widget):
	global sechand,minhand,houhand
	karamba.createImage(widget,0,0,"dial.png")
	#hand parameter: widget,hand image,shadow image,scale factor,x coord of pivot in hand image, same in y, x coord of pivot in background image, sam in y, offset for shadow
	# the scale factor shrinks the hand image (for anti-alias) so hands should be drawn larger than required
	# shadow image must be of the same size a hand image; make hand image a little larger as needed for blurring
	houhand=Hand(widget,"hhand.png","hhands.png",0.18,0.0,5.0,75,92,3)
	minhand=Hand(widget,"mhand.png","mhands.png",0.23,0.0,5.0,75,92,4)
#	sechand=Hand(widget,"shand.png","shands.png",0.27,15.0,5.0,75,92,4) # disable me if you don't want a sec hand 
	karamba.createImage(widget,0,0,"cover.png") # the center should be coverd since the hands are 'dancing' a little
	
def widgetUpdated(widget):
	time_tuple = time.localtime()
	hours = time_tuple[3]
	minutes = time_tuple[4]
	seconds = time_tuple[5]
	houhand.draw (widget,(hours-3)*30+int(minutes/5)*2.5)
	minhand.draw (widget,(minutes-15)*6+int(seconds/15)*1.5)
#	sechand.draw (widget,(seconds-15)*6) # disable me if you don't want a sec hand 


def widgetClosed(widget):
    pass
    
def widgetClicked(widget, x, y, button):
    pass

def widgetMouseMoved(widget, x, y, button):
    pass

def menuItemClicked(widget, menu, id):
    pass

def menuOptionChanged(widget, key, value):
    pass

def meterClicked(widget, meter, button):
    pass

def commandOutput(widget, pid, output):
    pass

def itemDropped(widget, dropText):
    pass

def startupAdded(widget, startup):
    pass
 
def startupRemoved(widget, startup):
    pass

def taskAdded(widget, task):
    pass

def taskRemoved(widget, task):
    pass

def activeTaskChanged(widget, task):
    pass

print "crystalclock by Skeezo"

