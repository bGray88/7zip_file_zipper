'''
Created on May 29, 2015

@author: bgray
'''

import os
import shutil
import site
import sys
import subprocess
import LogFile

from os.path import normpath
from os.path import join

class FileProcessor():
    
    def __init__(self, mDirectory, zipFormat, zipType, deleteOkay, fileType=''):
        self.deleteOriginal = deleteOkay
        self.selectedDirectory = (normpath(join(mDirectory)))
        self.originalZipFilename = (os.path.basename(self.selectedDirectory))
        self.mainDirectory = (os.path.dirname(self.selectedDirectory) + (normpath('\\')))
        self.zipProgramPath = (normpath(join(self.getDataFile(filename='prgms'), '7-Zip', '7zg.exe')))
        self.zipFormat = zipFormat
        self.zipType = zipType
        self.fileType = fileType
        self.zip7ZipFlags = "a -t7z -mx9 -m0=lzma2 -md=128m -mfb=128 -ms=on -mmt2"
        self.zipZipFlags = "a -tzip"
        self.processComplete = False
        self.processSuccess = True
        self.logFile = LogFile.LogFile(normpath(join(self.getDataFile())), '_7Zip_Zipper')
        
    def processFiles(self):
        self.logFile.logMsg('\n-----------------\n'
                            'Zip Processes\n'
                            '-----------------\n')
        
        self.setZipType()
        self.startZipping()        
        
        return (self.processSuccess, '')
        
    def deleteFile(self, filePath):
        os.remove(filePath)
        self.logFile.logMsg('Deleted: ' + filePath + ' -> ' + 'Deleted' + '\n')
        
    def deleteFolder(self, folderPath):
        shutil.rmtree(folderPath, ignore_errors=True)
        self.logFile.logMsg('Deleted: ' + folderPath + ' -> ' + 'Deleted' + '\n')
        
    def setZipType(self):
        if self.zipType == '7ZIP':
            self.zipUseType = self.zip7ZipFlags
            self.strZipExt = ".7z"
        elif self.zipType == "ZIP":
            self.zipUseType = self.zipZipFlags
            self.strZipExt = ".zip"
            
    def startZipping(self):
        if self.zipFormat == 'SINGLE':
            self.selectedExt = self.getExtension(self.originalZipFilename)
            self.zipFilename = self.originalZipFilename.replace(self.getExtension(self.selectedDirectory), '')
            self.zipProcess()
            if self.deleteOriginal:
                if os.path.isfile(self.mainDirectory + self.zipFilename + self.strZipExt):
                    if (self.mainDirectory + self.zipFilename + self.selectedExt) != (self.mainDirectory + self.zipFilename + self.strZipExt):
                        self.deleteFile(self.mainDirectory + self.zipFilename + self.selectedExt)
        elif self.zipFormat == 'MULTI-SINGLE':
            self.mainDirectory = self.selectedDirectory + normpath('\\')
            fileNames = os.listdir(path=self.selectedDirectory)
            for file in fileNames:
                if self.getExtension(file) == self.fileType or self.fileType == '*':
                    if self.getExtension(file):
                        self.zipFilename = file.replace(self.getExtension(file), '')
                        self.selectedExt = self.getExtension(file)
                        self.zipProcess()
                        if self.deleteOriginal:
                            if os.path.isfile(self.mainDirectory + self.zipFilename + self.strZipExt):
                                if (self.mainDirectory + self.zipFilename + self.selectedExt) != (self.mainDirectory + self.zipFilename + self.strZipExt):
                                    self.deleteFile(self.mainDirectory + self.zipFilename + self.selectedExt)
                    else:
                        #Empty Folder
                        pass
        elif self.zipFormat == 'DIRECTORY':
            self.zipFilename = self.originalZipFilename
            self.selectedExt = (normpath('\\*'))
            self.zipProcess()
            if self.deleteOriginal:
                if os.path.isfile(self.mainDirectory + self.zipFilename + self.strZipExt):
                    self.deleteFolder(self.mainDirectory + self.zipFilename)
        elif self.zipFormat == 'RECURSE-DIRECTORY':
            self.recurseFolders(self.selectedDirectory)
            
    def recurseFolders(self, folderPath):
        listFolders = []
        listFiles = []
        listItems = os.listdir(folderPath)
        for item in listItems:
            if os.path.isdir(normpath(join(folderPath, item))):
                listFolders.append(normpath(join(folderPath, item)))
            else:
                listFiles.append(normpath(join(folderPath, item)))
                
        if not listItems:
            pass
        elif listFolders:
            for folder in listFolders:
                self.recurseFolders(folder)
        else:
            file = listFiles[0]
            self.mainDirectory = (os.path.dirname((os.path.dirname(file))) + (normpath('\\')))
            self.zipFilename = os.path.basename(os.path.dirname(file))
            self.selectedExt = (normpath('\\*'))
            self.zipProcess()
            if self.deleteOriginal:
            	if os.path.isfile(self.mainDirectory + self.zipFilename + self.strZipExt):
            		self.deleteFile(file)
            		if not os.listdir(self.mainDirectory + self.zipFilename):
            			self.deleteFolder(self.mainDirectory + self.zipFilename)
                            
    def zipProcess(self):
        subprocess.call(self.doubleQuotes(self.zipProgramPath) + ' ' + self.zipUseType + ' ' +
                         self.doubleQuotes(self.mainDirectory + self.zipFilename + self.strZipExt) + ' ' + 
                         self.doubleQuotes(self.mainDirectory + self.zipFilename + self.selectedExt))
        self.logFile.logMsg('Created: ' + self.mainDirectory + self.zipFilename + self.selectedExt + ' -> ' + 
                            self.mainDirectory + self.zipFilename + self.strZipExt + '\n')
        
    def doubleQuotes(self, strQuotes):
        return ('\"' + strQuotes + '\"')
        
    def getDataFile(self, path='', filename=''):
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = join(site.getsitepackages()[0], path)
        return (normpath(join(datadir, filename)))
        
    def getFilename(self, originalFilePath):
        return os.path.basename(originalFilePath.replace(self.getExtension(originalFilePath), ''))
        
    def getExtension(self, filename):
        i = 0
        strIndex = 0
        fileExt = filename
        if fileExt.find('.', i) is not -1:
            while i is not len(fileExt):
                if fileExt.find('.', i) is not -1:
                    strIndex = fileExt.find('.', i)
                if strIndex > i:
                    i = strIndex
                else:
                    i = i + 1
            fileExt = fileExt[strIndex:len(fileExt)]
        else:
            fileExt = None
        return fileExt
        
    def getRootDir(self):
        rootDir = os.path.expanduser('~')
        rootIdx = rootDir.find(normpath('/'))
        while rootDir.find(normpath('/'), (rootIdx + 1)) is not -1:
            rootDir = os.path.dirname(rootDir)
        return (os.path.dirname(rootDir))
        
    def logError(self, failtag):
        self.processSuccess = False
        self.logFile.logMsg('\n\n**************************************\n'
                            '-THE PROCESS HAS FAILED-' + failtag + '\n'
                            '**************************************\n')
        return
        