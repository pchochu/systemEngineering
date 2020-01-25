import time
import numpy as np
from random import randrange
from queue import *
import variables as v
import output as o

class Simulation:
    qB = Queue(maxsize=v.capacityOfPointB)
    qC = 0
    qD = Queue(maxsize=v.capacityOfPointD)
    sE = {}
    sF = {}
    sG = {}
    totalNumOfPeople = 0
    unsatisfiedPeople = 0
    totalWaitingTimeAtPointC = 0

    def simulate(self):
        self.createDicts()
        self.start()
        o.createOutput(self.totalNumOfPeople, self.unsatisfiedPeople, v.numberOfPlacesAtTablesF, v.numberOfPlacesAtEAndGChairs)

    def start(self):
        for hour in range(v.openingHoursOfBuffet[0],v.openingHoursOfBuffet[1]):
            people = self.generatePeople()

            if hour < v.peakHours[0] or hour > v.peakHours[1]:
                peak = v.offPeakHoursDiscrimination
            else:
                peak = 1

            for minute in range(0, 60):
                
                numOfPeopleOnEtrance = np.count_nonzero(people == minute)
                self.peopleBehaviorOnEntrance(int(float(numOfPeopleOnEtrance)*peak))
                
                for second in range(0, 60):

                    self.handleQueueAtC() 
                    self.handleQueueAtD()
                    self.handlePlacesToSit()
                                
    def generatePeople(self):
        randNumOfPeople = randrange(v.minimumPplThatCanComePerHour, v.maximumPplThatCanComePerHour, 1)
        s = np.random.poisson(v.peakTimeInSpecificHour, randNumOfPeople)
        for num in range(0, len(s)):
            s[num] = s[num] if s[num] < 59 else s[num] - 59

        return s

    def peopleBehaviorOnEntrance(self, numOfPeopleOnEtrance):
        for person in range(0, numOfPeopleOnEtrance):
            randNum = randrange(0, 101, 1)
            if randNum < v.probThatNewcomerGoesToBuffet:
                self.isQueueFull(self.qB)
            elif randNum > v.probThatNewcomerGoesOutOfSys:
                self.addPersonToTotalNumberOfPeople()
            else:
                self.isQueueFull(self.qD)

    def handleQueueAtC(self):
        if self.qC - 1 == 0:
            randNum = randrange(0, 101, 1)
            if randNum < 70:
                self.addPersonToTotalNumberOfPeople()
            else:
                self.isQueueFull(self.qD)

        if self.qC != 0:
            self.qC = self.qC - 1
            self.totalWaitingTimeAtPointC = self.totalWaitingTimeAtPointC + 1
        elif not self.qB.empty():
            self.qB.get()
            self.qC = v.waitTimeInPointCInSeconds
        

    def handleQueueAtD(self):
        if not self.qD.empty():
            randNum = randrange(0, 101, 1)

            if randNum < 6:
                self.isPlaceToSit(self.sE, v.timeSpentAtChairsE)
            elif randNum > 79:
                self.isPlaceToSit(self.sG, v.timeSpentAtChairsG)
            else:
                self.isPlaceToSit(self.sF, v.timeSpentAtTablesF)
    
    def handlePlacesToSit(self):
        self.handlePlaceToSit(self.sE)
        self.handlePlaceToSit(self.sG)
        self.handlePlaceToSit(self.sF)

    def handlePlaceToSit(self, place):
        for key, value in place.items():
            if value != 0:
                place.update({key:value-1})
                if value - 1 == 0:
                    self.totalNumOfPeople = self.totalNumOfPeople + 1

    def isQueueFull(self, queue):
        if queue.full():
            self.addUnsatisfiedPerson(queue)
            return True
        else: 
            queue.put(1)
            return False
    
    def isPlaceToSit(self, s, time):
        for key, value in s.items():
            if value == 0:
                s.update({key: time})
                self.qD.get()
                return True
        self.qD.get()
        self.addUnsatisfiedPersonToSit()
    
    def addPersonToTotalNumberOfPeople(self):
        self.totalNumOfPeople = self.totalNumOfPeople + 1

    def addUnsatisfiedPersonToSit(self):
        self.totalNumOfPeople = self.totalNumOfPeople + 1
        self.unsatisfiedPeople = self.unsatisfiedPeople + 1

    def addUnsatisfiedPerson(self, queue):
        queue.get()
        self.totalNumOfPeople = self.totalNumOfPeople + 1
        self.unsatisfiedPeople = self.unsatisfiedPeople + 1
    
    def createDicts(self):
        for x in range(0,v.numberOfPlacesAtEAndGChairs):
            self.sE.update({x:0})
            self.sG.update({x:0})
        for x in range(0,v.numberOfPlacesAtTablesF):
            self.sF.update({x:0})

    def printTime(self, h, m, s):
        secondsToShow = '0' + str(s) if s < 10 else str(s)
        minutesToShow = '0' + str(m) if m < 10 else str(m)
        hoursToShow = str(h)

        print(hoursToShow +':' + minutesToShow + ':'+ secondsToShow)

    
