import time
from UIElements.ClockNumber import *
from UIElements.TextItem import *
from UIElements.Dicts import *
import threading
import pygame
class ClockFunc(threading.Thread):
    ISOTIMEFORMAT="%Y-%m-%d %X"
    ClockNumbers = ClockNumberDict
    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context
        # stepHori = self.screenWidth / 20        self.loadImg()

        # stepVert = self.screenHight / 20
        # location31 = [stepHori / 4 * 40, stepVert * 6]
        # location32 = [stepHori / 4 * 40,  stepVert * 8]

        self.now = time.localtime()
        self.year = self.now.tm_year
        self.mon = self.now.tm_mon
        self.day = self.now.tm_mday
        self.hour =  self.now.tm_hour
        self.minute =  self.now.tm_min
        self.second =  self.now.tm_sec

        self.numberDict = CreateClockNumberDict(self.context.getScreenSize(), self.ClockNumbers, ( self.hour / 10, self.hour % 10, self.minute / 10, self.minute % 10))
        self.colon = CreateColon(self.context.getScreenSize(), self.second % 2 == 0)
        self.context.addDictForDisplay(self.numberDict)
        self.context.addElemForDisplay(self.colon)

        fileObj = open('Resources/database/schedule/%d-%d-%d.txt'%(self.year, self.mon, self.day))
        fileLines = fileObj.readlines()
        self.scheduleText = createTextItem(self.context.getScreenSize(), fileLines, ScheduleIndex, True)
        self.context.addDictForDisplay(self.scheduleText)
    def run(self):
        while True:
            now = time.localtime()
            year = now.tm_year
            mon = now.tm_mon
            day = now.tm_mday
            hour = now.tm_hour
            minute = now.tm_min
            second = now.tm_sec
            self.colon.active = second % 2 == 0
            if(hour, minute) != (self.hour, self.minute): #update time
                self.hour = hour
                self.minute = minute
                tmp = self.numberDict.values()
                tmp.sort(cmp = None, key = lambda x: x.name, reverse = False)
                map(lambda x: x[0].changeValue(x[1]), zip(tmp, (self.hour / 10, self.hour % 10, self.minute / 10, self.minute % 10)))

            # if(year, mon, day) != (self.year, self.mon, self.day):
            #     self.year = year
            #     self.mon = mon
            #     self.day = day
            #     fileObj = open('Resources/database/schedule/%d-%d-%d.txt'%(self.year, self.mon, self.day))
            #     fileLines = file_obj.read()
            #     self.scheduleText.changeText(fileLines)
