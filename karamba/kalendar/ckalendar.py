from time import localtime, strftime
from calendar import monthcalendar
import karamba

class cKalendar:
	def __init__(self):
		self.thisYear = localtime()[0]
		self.thisMonth = localtime()[1]
		self.thisWeekday = localtime()[6]
		self.thisDay = localtime()[2]
		self.monthString = strftime("%B", localtime())
		self.yearString = strftime("%Y", localtime())
		i = 0
		self.dayArray = ["", "", "", "", "", "", ""]
		while i <= 6:
			self.dayArray[i] = strftime("%a", (0,0,0,0,0,0,i,0,0))[0:2]
			i = i + 1
		self.calendarArray = monthcalendar(self.thisYear,self.thisMonth)
	
	def updateClass(self):
		self.thisYear = localtime()[0]
		self.thisMonth = localtime()[1]
		self.thisWeekday = localtime()[6]
		self.thisDay = localtime()[2]
		self.monthString = strftime("%B", localtime())
		self.yearString = strftime("%Y", localtime())
		i = 0
		self.dayArray = ["", "", "", "", "", "", ""]
		while i <= 6:
			self.dayArray[i] = strftime("%a", (0,0,0,0,0,0,i,0,0))[0:2]
			i = i + 1
		self.calendarArray = monthcalendar(self.thisYear,self.thisMonth)
	
	def getDayCoords(self, day):
		j = 0
		e = -1
		f = -1
		while j <= 4 and f == -1:
			c = searchArray(self.calendarArray[j], day)
			if c != -1:
				e = c
				f = j
			j = j + 1
		g = [e,f]
		return g
	
	def printTop(self, widget, update):
		if update == 0:
			self.k_MonthCaption = karamba.createText(widget, 25, 17, 200, 50, self.monthString)
			karamba.changeTextColor(widget, self.k_MonthCaption, 255, 255, 255)
			karamba.changeTextSize(widget, self.k_MonthCaption, 20)
			self.k_YearCaption = karamba.createText(widget, 160, 17, 200, 50, self.yearString)
			karamba.changeTextColor(widget, self.k_YearCaption, 255, 255, 255)
			karamba.changeTextSize(widget, self.k_YearCaption, 22)
		else:
			karamba.changeText(widget, self.k_MonthCaption, self.monthString)
			karamba.changeText(widget, self.k_YearCaption, self.yearString)
			
	
	def showWeekImage(self, widget, update):
		if update == 0:
			self.k_weekImage = karamba.createImage(widget, self.xMark[self.getDayCoords(self.thisDay)[0]], 50, "images/weekmark.png")
		else:
			karamba.moveImage(widget, self.k_weekImage, self.xMark[self.getDayCoords(self.thisDay)[0]], 50)
	
	def showDayMarker(self, widget, update):
		if update == 0:
			self.k_dayMarker = karamba.createImage(widget, self.xMark[self.getDayCoords(self.thisDay)[0]], self.yMark[self.getDayCoords(self.thisDay)[1]], "images/daymark.png")
		else:
			karamba.moveImage(widget, self.k_dayMarker, self.xMark[self.getDayCoords(self.thisDay)[0]], self.yMark[self.getDayCoords(self.thisDay)[1]])
	
	def printDayCaptions(self, widget, update):
		if update != 0:
			i = 0
			while i <= 6:
				karamba.deleteText(widget, self.k_dayCaption[i])
				i = i + 1
		i = 0
		while i <= 6:
			self.k_dayCaption[i] = karamba.createText(widget, self.xPosition[i], 50, 200, 50, self.dayArray[i])
			karamba.changeTextFont(widget, self.k_dayCaption[i], "arialbd")
			karamba.changeTextColor(widget, self.k_dayCaption[i], 255, 255, 255)
			i = i + 1
		karamba.changeTextColor(widget, self.k_dayCaption[self.thisWeekday], 255, 255 , 255)
	
	def printCalendar(self, widget, update):
		if update != 0:
			j = 0
			while j <= 4:
				i = 0
				while i <= 6:
					karamba.deleteText(widget, self.k_dayField[j][i])
					i = i + 1
				j = j + 1
		j = 0
		while j <= 4:
			i = 0
			while i <= 6:
				self.k_dayField[j][i] = karamba.createText(widget, self.xPosition[i], 	self.yPosition[j], 200, 50, str(self.calendarArray[j][i]))
				karamba.changeTextColor(widget, self.k_dayField[j][i], 255, 255, 255)
				karamba.changeTextFont(widget, self.k_dayField[j][i], "Arial")
				if self.calendarArray[j][i] == 0:
					karamba.hideText(widget, self.k_dayField[j][i])
				i = i + 1
			j = j + 1
	
	def colorizeWeek(self, widget, r, g, b):
			i = 0
			while i <= 4:
				karamba.changeTextColor(widget, self.k_dayField[i][self.thisWeekday], r, g , b)
				i = i + 1	#print calendar.getDayCoords(20)

	def colorizeDay(self, widget, day, r, g, b):
		karamba.changeTextColor(widget, self.k_dayField[self.getDayCoords(day)[1]][self.getDayCoords(day)[0]], r, g, b) 
	
	xPosition = [22, 51, 80, 106, 133, 161, 189]
	yPosition = [69, 88, 107, 126, 145]
	xMark = [19, 48, 76, 103, 131, 158, 186]
	yMark = [68, 87, 106, 125, 144]
	k_dayCaption = [0, 0, 0, 0, 0, 0, 0]
	k_dayField = [0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]

def searchArray(sArray, fContent):
	# unfortunately the index() function doesn't work if the searched value
	# doesn't exist, so we have to create our own. It returns -1 if the value
	# was not found.
	x = len(sArray)
	i = 0
	e = -1
	while i <= (x - 1):
		if sArray[i] == fContent:
			e = i
		i = i + 1
	return e