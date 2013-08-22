# encoding=utf-8

import Tkinter
import sys
import tkFileDialog
import xerox
import tkMessageBox
import threading
import subprocess
import time
import os

ProgramPath=sys.argv[0][0:sys.argv[0].rfind('/')]#no final "/"
DownloadProgram=ProgramPath+'/youtube-dl'
DownloadPathDefault=ProgramPath+'/Downloads/'
#DoenloadArrayLock=threading.Lock()
###################################################################
#选择下载路径
def ChooseDownloadPath():
    DownloadPath=tkFileDialog.askdirectory(\
        title="Choose Download Path",initialdir=DownloadPathDefault)
    if DownloadPath:
        if DownloadPath[len(DownloadPath)-1]!='/':
            DownloadPath=DownloadPath+'/'
        DownloadPathEntry.delete('0','end')
        DownloadPathEntry.insert('end',DownloadPath)
    else:
        tkMessageBox.showwarning('Choose a Download Path',\
                                 "Please choose a download path. Otherwise, %s will be used"%DownloadPathDefault)
####################################################################
#拷贝URL
def PasteURL():
    URL=xerox.paste()
    DownloadURLEntry.delete("0","end")
    DownloadURLEntry.insert("end",URL)
##################################################################
#下载任务
#class DownloadTask(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
###################################################################
#Download
def DownloadProcess(DownloadURL,DownloadPath):
    if DownloadURL[0:4]!="http" and DownloadURL[0:5]!="https":
        tkMessageBox.showwarning("Wrong URL","%s is not a correct URL (include http or https)" \
                                             %DownloadURL)
    else:
        P=subprocess.Popen("%s --newline %s -o '%s"%(DownloadProgram,DownloadURL,DownloadPath)+"%(title)s.%(ext)s'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        DownloadInfo.delete(1.0,"end")
        DownloadButton['state']='disable'
        while P.stdout.readline()!='':
            P.stdout.readline()
            DownloadInfo.insert(1.0,"%s\n"%P.stdout.readline())
            if P.stdout.readline().find("Error")>=0 or P.stdout.readline().find("error")>=0 or P.stdout.readline().find("ERROR")>=0:
                tkMessageBox.showwarning("Downlad Fail","There is something wrong. Please double check inputs.")
                break
                time.sleep(1)
        DownloadInfo.insert(1.0,"%s\n"%"Finish!!")
        DownloadButton['state']='normal'
#开始下载
def BeginDownload():
    DownloadPath=DownloadPathEntry.get()
    DownloadURL=DownloadURLEntry.get()
    if os.path.exists(DownloadPath):
        t=threading.Thread(target=DownloadProcess,args=(DownloadURL,DownloadPath))
        t.start()
    else:
        if tkMessageBox.askquestion("Wrong Path",\
                                 "There isn't %s. Would you like to create it?"%DownloadPath)=='yes':
            try:
                os.makedirs(DownloadPath)
                t=threading.Thread(target=DownloadProcess,args=(DownloadURL,DownloadPath))
                t.start()
            except:
                tkMessageBox.showwarning("Wrong Path","%s is not a path"\
                    %DownloadPath)
###################################################################
#打开文件夹
def OpenDir():
    DownloadPath=DownloadPathEntry.get()
    if os.path.exists(DownloadPath):
        os.system("open %s"%DownloadPath)
    else:
        if tkMessageBox.askquestion("Wrong Path", \
                                    "There isn't %s. Would you like to create it?"%DownloadPath)=='yes':
            try:
                os.makedirs(DownloadPath)
                os.system("open %s"%DownloadPath)
            except:
                tkMessageBox.showwarning("Wrong Path","%s is not a path" \
                                                      %DownloadPath)
#######################################################################

#主程序
root=Tkinter.Tk()

DownloadPathFrame=Tkinter.Frame(root)
DownloadPathFrame.pack()
DownloadPathLabel=Tkinter.Label(DownloadPathFrame,text='Download Path: ')
DownloadPathLabel.pack(side='left')
DownloadPathEntry=Tkinter.Entry(DownloadPathFrame)
DownloadPathEntry.pack(side="left")
DownloadPathEntry.insert('end',DownloadPathDefault)
DownloadPathButton=Tkinter.Button(DownloadPathFrame,text='...',command=ChooseDownloadPath)
DownloadPathButton.pack(side="left")

DownloadURLFrame=Tkinter.Frame(root)
DownloadURLFrame.pack()
DownloadURLLabel=Tkinter.Label(DownloadURLFrame,text='Download URL:',width=15)
DownloadURLLabel.pack(side="left")
DownloadURLEntry=Tkinter.Entry(DownloadURLFrame)
DownloadURLEntry.pack(side="left")
DownloadURLButton=Tkinter.Button(DownloadURLFrame,text="Paste",command=PasteURL)
DownloadURLButton.pack(side="left")

ControlFrame=Tkinter.Frame(root)
ControlFrame.pack()
DownloadButton=Tkinter.Button(ControlFrame,text='Download',command=BeginDownload)
DownloadButton.pack(side="left")
OpenButton=Tkinter.Button(ControlFrame,text="Open in the finder",command=OpenDir)
OpenButton.pack(side="left")

DownloadInfo=Tkinter.Text(root,width=42)
DownloadInfo.pack()

#DownloadArrayFrame=Tkinter.Frame(root)
#DownloadArrayFrame.pack()
#DownloadArray=Tkinter.Listbox(DownloadArrayFrame,width=42)
#DownloadArray.pack(side="left")
#sl=Tkinter.Scrollbar(DownloadArrayFrame)
#sl.pack(side="left",fill="y")
#DownloadArray['yscrollcommand'] = sl.set
#sl['command'] = DownloadArray.yview

root.mainloop()