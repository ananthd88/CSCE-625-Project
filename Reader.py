#!/usr/bin/python
import csv

class Reader:
   def __init__(self, filename, perCount):
      self.filename = filename
      self.perCount = perCount
      self.resetAll()
      return   
   def resetAll(self):
      self.currentCount = 0
      self.fileHandle = None
      self.csvHandle = None
      self.csvIterator = None
      return
   def openFile(self):
      if self.fileHandle is not None:
         self.fileHandle.close()
      self.resetAll()
      self.fileHandle = open(self.filename, 'r')
      self.csvhandle = csv.DictReader(self.fileHandle)      
      self.csvIterator = self.csvhandle.__iter__()
      return
   def readNext(self):
      try:
         while self.currentCount % self.perCount:
            row = self.csvIterator.next()
            self.currentCount += 1
         row = self.csvIterator.next()
         self.currentCount += 1
      except StopIteration:
         return {}
      return row
   def closeFile(self):
      if self.fileHandle:
         self.fileHandle.close()
      self.resetAll()
