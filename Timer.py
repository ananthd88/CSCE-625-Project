import time
import sys
import math

class Timer:
   """Class to time function calls - Counts the CPU time used"""
   # Start the timer
   def __init__(self, string, limit = 100, numBars = 100):
      self.string = string
      self.beginning = time.clock()
      self.time  = 0.0
      self.numBars = numBars
      self.oneBar = 0
      self.numBarsWritten = 0
      self.limit = limit
      self.progress = 0
      if self.numBars:
         #print self.string
         self.oneBar = int(math.ceil(limit/numBars))
         sys.stdout.write("[%s]" % (" " * numBars))
         sys.stdout.flush()
         sys.stdout.write("\b" * (numBars + 1))
   
   def start(self, string, limit = 100, numBars = 100):
      self.__init__(string, limit, numBars)
      
   def getTime(self):
      if self.beginning:
         return time.clock() - self.beginning + self.time
      else:
         return self.time

   def stop(self):
      """"Print the CPU secs used"""
      if self.progress <= self.limit:
         sys.stdout.write('\x1b[2K')
         sys.stdout.write("\b" * (self.numBarsWritten + 2))
         self.progress = self.limit
      if self.beginning:
         timetaken = time.clock() - self.beginning + self.time
      else:
         timetaken = self.time
      print "\033[92mTime taken for (%s) = %f\033[0m" % (self.string, timetaken)
      self.string = None
      self.beginning = None
      self.time = None
      self.limit = 0
      self.progress = 0
      self.numBars = 0
      self.oneBar = 0
      return timetaken
      
   def tick(self):
      if self.beginning and self.progress < self.limit:
         self.progress += 1
         if self.oneBar and self.progress % self.oneBar == 0:
            if self.numBarsWritten < self.numBars:
               if (self.numBarsWritten + 1) % 10 == 0:
                  sys.stdout.write("|")
               else:
                  sys.stdout.write("-")
               sys.stdout.flush()
               self.numBarsWritten += 1
            else:
               self.progress = self.limit
               self.numBarsWritten = self.numBars
         #if self.progress == self.limit:
         #   sys.stdout.write('\x1b[2K')
         #   sys.stdout.write("\b" * (self.numBars + 2))
   
   def pause(self):
      if self.beginning:
         self.time += time.clock() - self.beginning
         self.beginning = None
   def unpause(self):
      if not self.beginning:
         self.beginning = time.clock()
