#!/usr/bin/python
import csv
import xml.etree.ElementTree as et

class Reader:
   def __init__(self, filename, perCount):
      self.filename = filename
      self.fileHandle = None
      self.perCount = perCount
      self.currentCount = 0      
      return   
   def reset(self):
      if self.fileHandle is not None:
         self.fileHandle.close()
      self.filename = None
      self.fileHandle = None
      self.perCount = None
      self.currentCount = 0
      return
   def closeFile(self):
      self.reset()
   def getNextRow(self):
      print "Inside dummy getNextRow() of Reader class"
      return {}
   def readNext(self):
      row = {}
      while self.currentCount % self.perCount:
         row = self.getNextRow()
         self.currentCount += 1
      row = self.getNextRow()
      self.currentCount += 1
      return row
   
class XMLReader(Reader):
   def __init__(self, filename, perCount):
      Reader.__init__(self, filename, perCount)
      self.xmlHandle = None
      self.xmlIterator = None
      return
   def resetAll(self):
      self.reset()
      self.xmlHandle = None
      self.xmlIterator = None
      return
   def openFile(self):
      # TODO: How to close this file handle
      self.xmlHandle = et.parse(self.filename)
      self.xmlIterator = self.xmlHandle.getroot()
      self.xmlIterator = self.xmlIterator.iter()
      self.xmlIterator.next()
      return
   def getNextRow(self):
      row = {}
      try:
         entry = self.xmlIterator.next()         
      except StopIteration:
         return row
      # TODO: Do this only if the row is likely to be fetched
      row["Id"] = entry.get('Id')
      row["Title"] = entry.get('Title')
      row["Body"] = entry.get('Body')
      row["Tags"] = entry.get('Tags')
      return row
      

class CSVReader(Reader):
   def __init__(self, filename, perCount):
      Reader.__init__(self, filename, perCount)
      self.csvHandle = None
      self.csvIterator = None
      return
   def resetAll(self):
      self.reset()
      self.csvHandle = None
      self.csvIterator = None
      return
   def openFile(self):
      self.fileHandle = open(self.filename, 'r')
      self.csvhandle = csv.DictReader(self.fileHandle)      
      self.csvIterator = self.csvhandle.__iter__()
      return
   def getNextRow(self):
      try:
         row = self.csvIterator.next()         
      except StopIteration:
         return {}
      return row
