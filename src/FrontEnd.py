'''
Created on May 29, 2015

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

import os
import threading
import App
import FileProcessor

from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL

from os.path import normpath
from os.path import join

class FrontEnd(App.App):
    
    def __init__(self):
        super().__init__()
        
        self.zipFormatSelected = None
        self.fileDirSelected = None
        self.zipTypeSelected = None
        self.fileTypeSelected = None
        self.returnsuccess = None
        self.returnMsg = None
        self.fileCompleteDelete = False
        
        self.container.setFrameIcon('7Zip.ico')
        
        self.displayIntroWindows()
        
    def resetSettings(self):
        self.procWindow.grid_remove()
        self.msgWindow.grid()
        
        self.processButton.config(state=DISABLED)
        self.zipFormatButton.config(state=NORMAL)
        self.zipTypeButton.config(state=NORMAL)
        self.dirSelectButton.config(state=DISABLED)
        self.fileTypeSelectButton.config(state=DISABLED)
        self.exitButton.config(state=NORMAL)
        
        self.statusMessageFiles.config(text='None' + '\n')
        self.statusMessageFormat.config(text='None' + '\n')
        self.statusMessageType.config(text='None' + '\n')
        self.statusMessageFileType.config(text='None' + '\n')
        
        self.zipFormatSelected = None
        self.zipTypeSelected = None
        self.fileDirSelected = None
        self.fileTypeSelected = None
        self.returnsuccess = None
        self.returnMsg = None
        
        self.checkDeleteButton.deselect()
        self.fileCompleteDelete = False
        
    def disableButtons(self):
        self.zipFormatButton.config(state=DISABLED)
        self.zipTypeButton.config(state=DISABLED)
        self.dirSelectButton.config(state=DISABLED)
        self.fileTypeSelectButton.config(state=DISABLED)
        self.processButton.config(state=DISABLED)
        self.exitButton.config(state=DISABLED)
        
    def displayIntroWindows(self):
        self.introBgdWindow()
        self.btnBgdWindow()
        self.statusBgdWindow()
        self.btnBtmWindow()
        self.statusBarBtmWindow()
        
    def checkProcessThread(self):
        if self.processThread.is_alive():
            self.container.after(1, self.checkProcessThread)
        else:
            self.progressBar.stop()
            self.progressBar.destroy()
            self.processResults()
            self.resetSettings()
        
    def runFileProcess(self):
        self.returnsuccess, self.returnMsg = self.fileProcessor.processFiles()
        
    def runFrontEndProcess(self):
        self.disableButtons()
        self.msgWindow.grid_remove()
        self.processBgdWindow()
        self.progressBar.start()
        self.fileProcessor = FileProcessor.FileProcessor(self.fileDirSelected, 
                                                         self.zipFormatSelected,
                                                         self.zipTypeSelected,
                                                         self.fileCompleteDelete, 
                                                         self.fileTypeSelected)
        self.processThread = threading.Thread(target=self.runFileProcess)
        self.processThread.daemon = True
        self.processThread.start()
        self.container.after(1, self.checkProcessThread)
        
    def startProcess(self):
        if self.zipFormatSelected:
            if self.zipTypeSelected:
                if self.fileDirSelected:
                    if self.zipFormatSelected == 'SINGLE':
                        self.runFrontEndProcess()
                    if self.zipFormatSelected == 'MULTI-SINGLE':
                        if self.fileTypeSelected:
                            self.runFrontEndProcess()
                        else:
                            tk.messagebox.showwarning('Open file', 
                                                      'Please select a valid File Type for Processing')
                    if self.zipFormatSelected == 'DIRECTORY':
                            self.runFrontEndProcess()
                    if self.zipFormatSelected == 'RECURSE-DIRECTORY':
                            self.runFrontEndProcess()
                else:
                    tk.messagebox.showwarning('Open file', 
                                              'Please select valid Files for Processing')
            else:
                tk.messagebox.showwarning('Open file', 
                                          'Please select a valid Zip Type')
        else:
            tk.messagebox.showwarning('Open file', 
                                      'Please select a valid Zip Format for Processing')
            
    def processResults(self):
        self.exitButton.config(state=NORMAL)
        unsuccessfulMsg = ('The process has finished unsuccessfully\n')
        successfulMsg = ('The process has finished successfully\n')
        suffixUnMsg = ('Please check your setup and attempt the process again\n')
        suffixMsg = ('Enjoy all of the newly created zipped files\n')
        
        if self.returnMsg is '#':
            completeMsg = (unsuccessfulMsg + '#\n' + suffixUnMsg)
        elif self.returnMsg is '#':
            completeMsg = (unsuccessfulMsg + '#\n' + suffixUnMsg)
        else:
            completeMsg = (successfulMsg + suffixMsg)
        tk.messagebox.showinfo('Process Complete', completeMsg)
        
    def checkProcessViabilty(self):
        if self.fileDirSelected and self.zipFormatSelected and self.zipTypeSelected:
            if self.zipFormatSelected != 'MULTI-SINGLE':
                self.processButton.config(state=NORMAL)
            elif self.zipFormatSelected == 'MULTI-SINGLE' and self.fileTypeSelected:
                self.processButton.config(state=NORMAL)
        
    def selectZipFormat(self):
        self.resetSettings()
        self.createTopLevel()
        selectButton = tk.Button(self.top, text="Select", command=self.setZipFormat,
                                 background='WHITE')
        
        self.top.title('Select Zip Format')
        MODES = [
                    ('SINGLE'),
                    ('MULTI-SINGLE'),
                    ('DIRECTORY'),
                    ('RECURSE-DIRECTORY')
                ]
        self.zipFormat = tk.StringVar()
        self.zipFormat.set('SINGLE')
        
        for text in MODES:
            radioLabel = tk.Radiobutton(self.top, text=text,
                            variable=self.zipFormat, value=text,
                            background='WHITE')
            radioLabel.pack(anchor='w')
        selectButton.pack(fill='both')
        
    def setZipFormat(self):
        self.zipFormatSelected = self.zipFormat.get()
        if self.zipFormatSelected != 'None':
            self.dirSelectButton.config(state=NORMAL)
        if self.zipFormatSelected == 'MULTI-SINGLE':
            self.fileTypeSelectButton.config(state=NORMAL)
        self.statusMessageFormat.config(text=self.zipFormatSelected + '\n')
        self.top.destroy()
        self.checkProcessViabilty()
        self.container.deiconify()
        
    def selectZipType(self):
        self.createTopLevel()
        selectButton = tk.Button(self.top, text="Select", command=self.setZipType, 
                                 background='WHITE')
        
        self.top.title('Select Zip Type')
        MODES = [
                    ('ZIP'),
                    ('7ZIP')
                ]
        self.zipType = tk.StringVar()
        self.zipType.set('ZIP')
        
        for text in MODES:
            radioLabel = tk.Radiobutton(self.top, text=text,
                            variable=self.zipType, value=text,
                            background='WHITE')
            radioLabel.pack(anchor='w')
        selectButton.pack(fill='both')
        
    def setZipType(self):
        self.zipTypeSelected = self.zipType.get()
        self.statusMessageType.config(text=self.zipTypeSelected + '\n')
        self.top.destroy()
        self.checkProcessViabilty()
        self.container.deiconify()
        
    def selectFileLocation(self):
        if self.zipFormatSelected:
            rootDir = self.getRootDir()
            self.container.withdraw()
            if self.zipFormatSelected == 'SINGLE':
                self.selectRequest = 'Select the File'
                self.fileDirSelected = self.browseForFile(self.selectRequest, normpath(rootDir))
                self.statusMessageFiles.config(text='...\\' + os.path.basename(self.fileDirSelected) + '\n')
            else:
                self.selectRequest = 'Select the File Directory'
                self.fileDirSelected = self.browseForFolder(self.selectRequest, True, 
                                                        normpath(rootDir))
                self.statusMessageFiles.config(text='...\\' + os.path.basename(self.fileDirSelected) + '\\' + '\n')
        else:
            tk.messagebox.showwarning('Open file', 
                                          'Please select valid Zip Format first')
        self.checkProcessViabilty()
        self.container.deiconify()
            
    def browseForFile(self, title, initialdir):
        return tk.filedialog.askopenfilename(title=title, 
                                          initialdir=initialdir)
        
    def browseForFolder(self, title, mustexist, initialdir):
        return tk.filedialog.askdirectory(title=title, 
                                          mustexist=mustexist, 
                                          initialdir=initialdir)
        
    def getRootDir(self):
        rootDir = os.path.expanduser('~')
        rootIdx = rootDir.find(normpath('/'))
        while rootDir.find(normpath('/'), (rootIdx + 1)) is not -1:
            rootDir = os.path.dirname(rootDir)
        return (os.path.dirname(rootDir))
        
    def selectFileType(self):
        self.labelFont = ('sans', 12, 'bold')
        self.createTopLevel()
        selectButton = tk.Button(self.top, text="Select", command=self.setFileType, 
                                 background='WHITE')
        
        self.top.title('Input File Type as Extension')
        self.inputLabel = tk.Label(self.top, width=0, height=0, padx=12, pady=12,
                                   background='WHITE', foreground='BLACK', font=self.labelFont,
                                   text='\nInput File Type as Extension\n')
        self.fileType = tk.StringVar()
        
        entryBox = tk.Entry(self.top, textvariable=self.fileType, background='WHITE')
        
        self.inputLabel.pack()
        entryBox.pack(anchor='n')
        selectButton.pack(anchor='n', fill='both')
        
    def setFileType(self):
        self.fileTypeSelected = self.fileType.get()
        if self.getExtension(str(self.fileTypeSelected)) == None:
            self.fileTypeSelected = '.' + self.fileTypeSelected
        if self.fileTypeSelected == '.':
            self.fileTypeSelected = '*'
        self.statusMessageFileType.config(text=self.fileTypeSelected + '\n')
        self.top.destroy()
        self.checkProcessViabilty()
        self.container.deiconify()
        
    def setDeleteFileState(self, event=None):
        self.fileCompleteDelete = self.checkVar.get()
        
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
        
    def createTopLevel(self):
        self.container.withdraw()
        self.top = tk.Toplevel()
        self.top.config(background='WHITE')
        self.top.protocol('WM_DELETE_WINDOW', self.removeTopLevel)
        self.top.lift()
        self.top.attributes('-topmost', True)
        
    def removeTopLevel(self):
        self.top.destroy()
        self.container.deiconify()
        
    def configWindows(self, window, *args):
        for coords in args:
            for rx, rw, cx, cw in coords:    
                window.gridConfig(rx, rw, cx, cw)
        
    def btnBgdWindow(self):
        ZIP_FORMAT_COMMAND = self.selectZipFormat
        ZIP_RADIO_COMMAND = self.selectZipType
        DIR_SELECT_COMMAND = self.selectFileLocation
        FILE_TYPE_SELECT_COMMAND = self.selectFileType
        self.zipFormatButton = self.bgdBtnWindow.createButton('Zip Format', 'WHITE', 
                                                 'BLACK', ZIP_FORMAT_COMMAND, '2', '25')
        self.zipTypeButton = self.bgdBtnWindow.createButton('Zip Type', 'WHITE', 
                                                 'BLACK', ZIP_RADIO_COMMAND, '2', '25')
        self.fileTypeSelectButton = self.bgdBtnWindow.createButton('File Type', 'WHITE', 
                                                 'BLACK', FILE_TYPE_SELECT_COMMAND, '2', '25')
        self.fileTypeSelectButton.config(state=DISABLED)
        self.dirSelectButton = self.bgdBtnWindow.createButton('File(s)', 'WHITE', 
                                                 'BLACK', DIR_SELECT_COMMAND, '2', '25')
        self.dirSelectButton.config(state=DISABLED)
        self.btnGridConfig = [[0,1,None,None], [1,1,None,None], 
                              [2,1,None,None], [3,1,0,1]]
        self.configWindows(self.bgdBtnWindow, self.btnGridConfig)
        self.bgdBtnWindow.placeButton(self.zipFormatButton, 0, 0, 'nsew')
        self.bgdBtnWindow.placeButton(self.zipTypeButton, 1, 0, 'nsew')
        self.bgdBtnWindow.placeButton(self.dirSelectButton, 2, 0, 'nsew')
        self.bgdBtnWindow.placeButton(self.fileTypeSelectButton, 3, 0, 'nsew')
        self.bgdWindow.addWindow(self.bgdBtnWindow, 0, 0, 'nsew')
        
    def introBgdWindow(self):
        self.labelFont = ('sans', 12, 'bold')
        self.introMessage = tk.Label(self.msgWindow, width=0, height=0, padx=12, pady=12,
                                   background='WHITE', foreground='BLACK', font=self.labelFont,
                                   text='\nWelcome to the 7Zip File Zipper\n'
                                   'Simply select your preferred zip format \n '
                                   'and zip type, select a file location \n'
                                   'or a file itself, and then process your files\n\n')
        self.msgGridConfig = [[0,1,0,1]]
        self.configWindows(self.msgWindow, self.msgGridConfig)
        self.msgWindow.addWindow(self.introMessage, 0, 0, 'n')
        self.bgdWindow.addWindow(self.msgWindow, 0, 1, 'nsew')
        
    def processBgdWindow(self):
        self.labelFont = ('sans', 12, 'bold')
        self.procMessage = tk.Label(self.procWindow, width=0, height=0, padx=12, pady=12,
                                   background='WHITE', foreground='BLACK', font=self.labelFont,
                                   text='\nThe program will now process your files based\n'
                                   'on the destination/files selected\n')
        self.progressBar = tk.ttk.Progressbar(self.procWindow, orient='horizontal',
                                        length=(int(self.windowedWidth / 2)), 
                                        mode='indeterminate')
        self.procGridConfig = [[0,1,None,None], [1,1,None,None], 
                              [2,1,None,None], [3,1,None,None],
                              [4,1,0,1]]
        self.configWindows(self.procWindow, self.procGridConfig)
        self.procWindow.addWindow(self.procMessage, 1, 0, 'nsew')
        self.procWindow.addWindow(self.progressBar, 3, 0)
        self.bgdWindow.addWindow(self.procWindow, 0, 1, 'nsew')
        
    def statusBgdWindow(self):
        self.labelFont = ('sans', 12, 'bold')
        PROCESS_COMMAND = self.startProcess
        self.statusMessageBase = tk.Label(self.bgdStsWindow, width=0, height=0, padx=12, pady=12,
                                          background='BLACK', foreground='WHITE', font=self.labelFont,
                                          text=('Process Structure\n'
                                                '---------------------------\n'))
        self.labelFont = ('helvetica', 10)
        self.statusMessageFormat = tk.Label(self.bgdStsWindow, width=0, height=0, 
                                          background='BLACK', foreground='WHITE', font=self.labelFont,
                                          text=(str(self.zipFormatSelected) + '\n'))
        self.statusMessageType = tk.Label(self.bgdStsWindow, width=0, height=0, 
                                          background='BLACK', foreground='WHITE', font=self.labelFont,
                                          text=(str(self.zipTypeSelected) + '\n'))
        self.statusMessageFiles = tk.Label(self.bgdStsWindow, width=0, height=0, 
                                          background='BLACK', foreground='WHITE', font=self.labelFont,
                                          text=(str(self.fileDirSelected) + '\n'))
        self.statusMessageFileType = tk.Label(self.bgdStsWindow, width=0, height=0, 
                                          background='BLACK', foreground='WHITE', font=self.labelFont,
                                          text=(str(self.fileTypeSelected) + '\n'))
        self.processButton = self.bgdStsWindow.createButton('Process', 'WHITE', 
                                                 'BLACK', PROCESS_COMMAND, '4', '25')
        self.processButton.config(state=DISABLED)
        self.stsGridConfig = [[0,1,None,None], [1,1,None,None], 
                              [2,1,None,None], [3,1,None,None], 
                              [4,1,None,None], [5,1,0,1],
                              [6,1,0,1]]
        self.configWindows(self.bgdStsWindow, self.stsGridConfig)
        self.bgdStsWindow.addWindow(self.statusMessageBase, 0, 0, 'nsew')
        self.bgdStsWindow.addWindow(self.statusMessageFormat, 1, 0, 'nsew')
        self.bgdStsWindow.addWindow(self.statusMessageType, 2, 0, 'nsew')
        self.bgdStsWindow.addWindow(self.statusMessageFiles, 3, 0, 'nsew')
        self.bgdStsWindow.addWindow(self.statusMessageFileType, 4, 0, 'nsew')
        self.bgdStsWindow.placeButton(self.processButton, 5, 0, 'nsew')
        self.bgdWindow.addWindow(self.bgdStsWindow, 0, 2, 'nsew')
        
    def btnBtmWindow(self):
        self.checkVar = tk.BooleanVar()
        self.checkDeleteButton = tk.Checkbutton(self.btmBtnWindow, 
                                                text="Delete Original Files", 
                                                variable=self.checkVar, 
                                                command=self.setDeleteFileState, 
                                                bg='BLACK', activebackground='BLACK',
                                                fg='WHITE', activeforeground='WHITE',
                                                selectcolor='BLACK'
                                                )
        EXIT_COMMAND = self.endApp
        self.exitButton = self.btmBtnWindow.createButton('Exit', 'WHITE', 
                                                 'BLACK', EXIT_COMMAND, '2', '0')
        self.btmGridConfig = [[None,None,0,1], [0,1,1,1]]
        self.configWindows(self.btmBtnWindow, self.btmGridConfig)
        self.btmBtnWindow.placeButton(self.checkDeleteButton, 1, 0, 'nsew')
        self.btmBtnWindow.placeButton(self.exitButton, 1, 1, 'nsew')
        self.container.addWindow(self.btmBtnWindow, 1, 0, 'nsew')
        
    def statusBarBtmWindow(self):
        self.statusBar.setTitle('7Zip File Zipper')
        self.statusBar.setScreen('Menu')
        self.statusBar.padConfig(1, 1)
        self.statGridConfig = [[None,None,0,5], [None,None,1,5], 
                              [None,None,2,5], [None,None,3,5],
                              [0,1,4,3]]
        self.configWindows(self.statusBar, self.statGridConfig)
        self.container.addWindow(self.statusBar, 2, 0, 'nsew', 2)
        