#!/usr/bin/python2.7
# encoding=utf-8

import Tkinter
import sys
import tkFileDialog
import xerox
import tkMessageBox
import tkSimpleDialog
import threading
import subprocess
import time
import os

k=1
ProgramPath=sys.argv[0][0:sys.argv[0].rfind('/')]#no final "/"
DownloadProgram=ProgramPath+'/youtube-dl'
DownloadPathDefault=ProgramPath+'/Downloads/'
Options=["--playlist-start NUMBER    playlist video to start at (default is 1)",
         "--playlist-end NUMBER      playlist video to end at (default is last)",
         "--match-title REGEX        download only matching titles (regex or caseless sub-string)",
         "--reject-title REGEX       skip download for matching titles (regex or caseless sub-string)",
         "--max-downloads NUMBER     Abort after downloading NUMBER files",
         "--min-filesize SIZE        Do not download any videos smaller than SIZE (e.g. 50k or 44.6m)",
         "--max-filesize SIZE        Do not download any videos larger than SIZE (e.g. 50k or 44.6m)",
         "--date DATE                download only videos uploaded in this date",
         "--datebefore DATE          download only videos uploaded before this date",
         "--dateafter DATE           download only videos uploaded after this date",
         "-r LIMIT     maximum download rate (e.g. 50k or 44.6m)",
         "-R RETRIES      number of retries (default is 10)",
         "--buffer-size SIZE         size of download buffer (e.g. 1024 or 16k) (default is 1024)",
         "-t    use title in file name (default)",
         "--id    use only video ID in file name",
         "-A    number downloaded files starting from 00000",
         "-w    do not overwrite files",
         "-c    resume partially downloaded files",
         "--no-continue    do not resume partially downloaded files (restart from beginning)",
         "--no-part    do not use .part files",
         "--write-description        write video description to a .description file",
         "--write-info-json          write video metadata to a .info.json file",
         "--write-thumbnail          write thumbnail image to disk",
         "-g     simulate, quiet but print URL",
         "-e    simulate, quiet but print title",
         "--get-id    simulate, quiet but print id",
         "--get-thumbnail            simulate, quiet but print thumbnail URL",
         "--get-description          simulate, quiet but print video description",
         "--get-filename             simulate, quiet but print output filename",
         "--get-format               simulate, quiet but print output format",
         "--sub-lang LANG            language of the subtitles to download (optional) use IETF language tags like 'en'",
         "--audio-quality QUALITY    ffmpeg/avconv audio quality specification, inser a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)"]
DownloadArrayLock=threading.Lock()
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
class DownloadTask(threading.Thread):
    def __init__(self,DownloadProgram,DownloadURL,DownloadPath,DownloadOptions):
        threading.Thread.__init__(self)
        #定义变量
        self.Program=DownloadProgram
        self.name='Waiting'
        self.speed="--"
        self.path=DownloadPath
        self.process="0%"
        self.size="--"
        self.ETA="--"
        self.URL=DownloadURL
        self.Options=DownloadOptions
        self.position=DownloadArray.size()
        #打印信息
        DownloadArrayLock.acquire()
        Info="Name: %s  Speed: %s  %s of %s ETA: %s  Path: %s"%(self.name,self.speed,self.process,self.size,self.ETA,self.path)
        DownloadArray.insert(self.position,Info)
        DownloadArrayLock.release()
        if self.URL[0:4]!="http" and self.URL[0:5]!="https":
            tkMessageBox.showwarning("Wrong URL","%s is not a correct URL (include http or https)" \
                                                 %self.URL)
            DownloadArrayLock.acquire()
            DownloadArray.delete(self.position)
            DownloadArrayLock.release()
        else:
            P=subprocess.Popen("%s %s -e -s"%(self.Program,self.URL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.name=P.stdout.readline()[0:P.stdout.readline().find('\n')]
    def run(self):
        Error=0
        TaskWrong=0
        for Num in range(0,DownloadArray.size()-1):
            while DownloadArray.get(Num)[DownloadArray.get(Num).find('Name:')+6:DownloadArray.get(Num).find('Speed:')-2]=="Waiting":
                if k==0:
                    break
                else:
                    pass
            while self.name=='Waiting':
                if k==0:
                    break
                else:
                    pass
            if self.name==DownloadArray.get(Num)[DownloadArray.get(Num).find('Name:')+6:DownloadArray.get(Num).find('Speed:')-2]:
                TaskWrong=1
        if self.URL[0:4]!="http" and self.URL[0:5]!="https":
            pass
        elif k==0:
            pass
        elif TaskWrong:
            tkMessageBox.showwarning("Warning","The task has been existed.")
            DownloadArray.delete(self.position)
        else:
            P=subprocess.Popen("%s --newline %s %s -o '%s"%(self.Program,self.Options,self.URL,self.path)+"%(title)s.%(ext)s'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            tmp=P.stdout.readline()
            while tmp!='':
                if tmp.find('Error')>=0 or tmp.find('error')>=0 or tmp.find('ERROR')>=0:
                    DownloadArrayLock.acquire()
                    try:
                        choosing=int(DownloadArray.curselection()[0])
                    except:
                        choosing=-1
                    DownloadArray.delete(self.position)
                    if self.position!=0:
                        if DownloadArray.get(self.position-1)=='':
                            if choosing>=self.position:
                                choosing=choosing-1
                            self.position=self.position-1
                    Info="%s: Error  Path: %s"%(self.name,self.path)
                    DownloadArray.insert(self.position,Info)
                    DownloadArray.selection_set(choosing)
                    DownloadInfo.insert(1.0,'%s: Error. Please double check it\n'%self.name)
                    DownloadArrayLock.release()
                    Error=1
                elif tmp.find('ETA')>0:
                    self.speed=tmp[tmp.find('at')+4:tmp.find('ETA')-1]
                    self.process=tmp[tmp.find(']')+1:tmp.find('of')-1]
                    self.size=tmp[tmp.find('of')+3:tmp.find('at')-1]
                    self.ETA=tmp[tmp.find('ETA')+4:len(tmp)]
                    DownloadArrayLock.acquire()
                    try:
                        choosing=int(DownloadArray.curselection()[0])
                    except:
                        choosing=-1
                    DownloadArray.delete(self.position)
                    if self.position!=0:
                        if DownloadArray.get(self.position-1)=='':
                            if choosing>=self.position:
                                choosing=choosing-1
                            self.position=self.position-1
                    Info="Name: %s  Speed: %s  %s of %s ETA: %s  Path: %s"%(self.name,self.speed,self.process,self.size,self.ETA,self.path)
                    DownloadArray.insert(self.position,Info)
                    DownloadArray.selection_set(choosing)
                    DownloadInfo.insert(1.0,"%s: %s\n"%(self.name,tmp))
                    DownloadArrayLock.release()
                tmp=P.stdout.readline()
            if Error:
                tmp=DownloadArray.get(self.position)
                while k:
                    DownloadArrayLock.acquire()
                    if tmp==DownloadArray.get(self.position):
                        if self.position!=0:
                            if DownloadArray.get(self.position-1)=='':
                                self.position=self.position-1
                                DownloadArray.delete(self.position+1)
                                DownloadArray.insert(self.position,tmp)
                        DownloadArrayLock.release()
                        time.sleep(3)
                    else:
                        DownloadArrayLock.release()
                        break
            else:
                DownloadArrayLock.acquire()
                DownloadArray.delete(self.position)
                if self.position!=0:
                    if DownloadArray.get(self.position-1)=='':
                        self.position=self.position-1
                Info="%s: finish!! Path: %s"%(self.name,self.path)
                DownloadArray.insert(self.position,Info)
                DownloadInfo.insert(1.0,'%s: finish!!\n'%self.name)
                DownloadArrayLock.release()
                tmp=DownloadArray.get(self.position)
                while k:
                    DownloadArrayLock.acquire()
                    if tmp==DownloadArray.get(self.position):
                        if self.position!=0:
                            if DownloadArray.get(self.position-1)=='':
                                self.position=self.position-1
                                DownloadArray.delete(self.position+1)
                                DownloadArray.insert(self.position,tmp)
                        DownloadArrayLock.release()
                        time.sleep(3)
                    else:
                        DownloadArrayLock.release()
                        break
###################################################################
#Download
#def DownloadProcess(DownloadURL,DownloadPath,DownloadOptions):
#    if DownloadURL[0:4]!="http" and DownloadURL[0:5]!="https":
#        tkMessageBox.showwarning("Wrong URL","%s is not a correct URL (include http or https)" \
#                                             %DownloadURL)
#    else:
#        P=subprocess.Popen("%s --newline %s %s -o '%s"%(DownloadProgram,DownloadOptions,DownloadURL,DownloadPath)+"%(title)s.%(ext)s'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#        DownloadInfo.delete(1.0,"end")
#        tmp=P.stdout.readline()
#        while tmp!='':
#            DownloadInfo.insert(1.0,"%s\n"%tmp)
#            if P.stdout.readline().find("Error")>=0 or P.stdout.readline().find("error")>=0 or P.stdout.readline().find("ERROR")>=0:
#                tkMessageBox.showwarning("Downlad Fail","There is something wrong. Please double check inputs.")
#                break
#            else:
#                tmp=P.stdout.readline()
#        DownloadInfo.insert(1.0,"%s\n"%"Finish!!")
#开始下载
def BeginDownload():
    DownloadButton['state']='disable'
    DownloadPath=DownloadPathEntry.get()
    DownloadURL=DownloadURLEntry.get()
    DownloadOptions=OptionsEntry.get()
    if os.path.exists(DownloadPath):
        DownloadTask(DownloadProgram,DownloadURL,DownloadPath,DownloadOptions).start()
    else:
        if tkMessageBox.askquestion("Wrong Path",\
                                 "There isn't %s. Would you like to create it?"%DownloadPath)=='yes':
            try:
                os.makedirs(DownloadPath)
                DownloadTask(DownloadProgram,DownloadURL,DownloadPath,DownloadOptions).start()
            except:
                tkMessageBox.showwarning("Wrong Path","%s is not a path"\
                    %DownloadPath)
    DownloadButton['state']='normal'
###################################################################
#打开文件夹
def OpenDir():
    if DownloadArray.curselection()==():
        DownloadPath=DownloadPathEntry.get()
    else:
        DownloadArrayLock.acquire()
        tmp=DownloadArray.get(DownloadArray.curselection()[0])
        DownloadArrayLock.release()
        DownloadPath=tmp[tmp.find('Path:')+6:len(tmp)]
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
#选择options
def ChooseOptions():
    global ChooseOptionsWindow
    ChooseOptionsWindow=Tkinter.Toplevel(root)
    ChooseOptionsLabel1=Tkinter.Label(ChooseOptionsWindow,\
                                     text="Please choose options: ")
    ChooseOptionsLabel1.pack()
    ChooseOptionsLabel2=Tkinter.Label(ChooseOptionsWindow,\
                                      text="(You can choose one or more options)")
    ChooseOptionsLabel2.pack()
    ChooseOptionsListboxFrame=Tkinter.Frame(ChooseOptionsWindow)
    ChooseOptionsListboxFrame.pack()
    global ChooseOptionsListbox
    ChooseOptionsListbox=Tkinter.Listbox(ChooseOptionsListboxFrame,selectmode="multiple",width=45)
    ChooseOptionsListbox.pack(side="left")
    ChooseOptionsListboxSl=Tkinter.Scrollbar(ChooseOptionsListboxFrame)
    ChooseOptionsListboxSl.pack(side="left",fill="y")
    ChooseOptionsListbox['yscrollcommand']=ChooseOptionsListboxSl.set
    ChooseOptionsListboxSl['command']=ChooseOptionsListbox.yview
    for i in Options:
        ChooseOptionsListbox.insert('end',i)
    ChooseOptionsListboxSlx=Tkinter.Scrollbar(ChooseOptionsWindow,orient='horizontal')
    ChooseOptionsListboxSlx.pack(fill="x")
    ChooseOptionsListbox['xscrollcommand']=ChooseOptionsListboxSlx.set
    ChooseOptionsListboxSlx['command']=ChooseOptionsListbox.xview

    ChooseOptionsControlFrame=Tkinter.Frame(ChooseOptionsWindow)
    ChooseOptionsControlFrame.pack()
    ChooseOptionsOKButton=Tkinter.Button(ChooseOptionsControlFrame,text="OK",command=ChooseOptionsOK)
    ChooseOptionsOKButton.pack(side="left")
    ChooseOptionsCancelButton=Tkinter.Button(ChooseOptionsControlFrame,text="Cancel",command=ChooseOptionsWindow.destroy)
    ChooseOptionsCancelButton.pack(side="left")
def ChooseOptionsOK():
    OptionsEntry.delete("0","end")
    for i in ChooseOptionsListbox.curselection():
        if Options[int(i)][0:Options[int(i)].find("    ")+1]=="--playlist-start NUMBER ":
            try:
                i="--playlist-start %s "%tkSimpleDialog.askinteger("Playlist Start","What is the playlist start number?")
                if i!="--playlist-start %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--playlist-end NUMBER ":
            try:
                i="--playlist-end %s "%tkSimpleDialog.askinteger("Playlist End","What is the playlist end number?")
                if i!="--playlist-end %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--match-title REGEX ":
            try:
                i="--match-title %s "%tkSimpleDialog.askstring("Title","What is the match title?")
                if i!="--match-title %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--reject-title REGEX ":
            try:
                i="--reject-title %s "%tkSimpleDialog.askstring("Title","What is the reject title?")
                if i!="--reject-title %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--max-downloads NUMBER ":
            try:
                i="--max-downloads %s "%tkSimpleDialog.askinteger("Max Downloads","What is the maximum download number?")
                if i!="--max-downloads %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--min-filesize SIZE ":
            try:
                i="--min-filesize %s "%tkSimpleDialog.askstring("Minimum file size", "What is the minimum file size?")
                if i!="--min-filesize %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--max-filesize SIZE ":
            try:
                i="--max-filesize %s "%tkSimpleDialog.askinteger("Maximum file size","What is the maximum file size?")
                if i!="--max-filesize %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--date DATE ":
            try:
                i="--date %s "%tkSimpleDialog.askstring("Video Upload Date","What is the date in which you want to download video?")
                if i!="--date %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--datebefore DATE ":
            try:
                i="--datebefore %s "%tkSimpleDialog.askstring("Video Upload Data","What is the date before which you want to download video?")
                if i!="--datebefore %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--dateafter DATE ":
            try:
                i="--dateafter %s "%tkSimpleDialog.askstring("Video Upload Data","What is the date after which you want to download video?")
                if i!="--dateafter %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="-r LIMIT ":
            try:
                i="-r %s "%tkSimpleDialog.askstring("Maximum speed","Waht is the maximum download speed?")
                if i!="-r %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="-R RETRIES ":
            try:
                i="-R %s "%tkSimpleDialog.askstring("Maximum number of retries","What is the maximum number of retries?")
                if i!="-R %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--buffer-size SIZE ":
            try:
                i="--buffer-size %s "%tkSimpleDialog.askstring("Maximum buffer size","What is the maximum buffer size?")
                if i!="--buffer-size %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--sub-lang LANG ":
            try:
                i="--sub-lang %s "%tkSimpleDialog.askstring("Language","what is the language that you want to download?")
                if i!="--sub-lang %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--audio-quality QUALITY ":
            try:
                i="--audio-quality %s "%tkSimpleDialog.askinteger("Quality","What is the Quality that you want to download?")
                if i!="--audio-quality %s "%None:
                    OptionsEntry.insert('end',i)
                else:
                    continue
            except:
                continue
        else:
            OptionsEntry.insert('end',Options[int(i)][0:Options[int(i)].find("    ")+1])
    ChooseOptionsWindow.destroy()
########################################################################
#关闭按钮
def callback(event=None):
    global k
    k=0
    DownloadArrayLock.acquire()
    DownloadInfo.insert(1.0,"I am closing.......\n")
    DownloadArrayLock.release()
    root.quit()
#######################################################################
#Delete Task
def DeleteTask():
    if DownloadArray.curselection()==():
        tkMessageBox.showwarning('Warning',"Please choose a download task")
    else:
        DownloadArrayLock.acquire()
        tmp=DownloadArray.get(DownloadArray.curselection()[0])
        DownloadArrayLock.release()
        if tmp.find('Error')>=0 or tmp.find('finish')>=0:
            DownloadArrayLock.acquire()
            choosing=DownloadArray.curselection()[0]
            DownloadArray.delete(choosing)
            if int(choosing)!=DownloadArray.size():
                DownloadArray.selection_set(choosing)
            else:
                DownloadArray.selection_set(int(choosing)-1)
            DownloadArrayLock.release()
        else:
            tkMessageBox.showwarning('Warning','This task has not been finished. Please waiting.')
#######################################################################



#主程序
root=Tkinter.Tk()

ControlLabelFrame=Tkinter.LabelFrame(root,text="Download Information")
ControlLabelFrame.pack(side="left",fill="y")

DownloadPathFrame=Tkinter.Frame(ControlLabelFrame)
DownloadPathFrame.pack()
DownloadPathLabel=Tkinter.Label(DownloadPathFrame,text='Download Path: ')
DownloadPathLabel.pack(side='left')
DownloadPathEntry=Tkinter.Entry(DownloadPathFrame)
DownloadPathEntry.pack(side="left")
DownloadPathEntry.insert('end',DownloadPathDefault)
DownloadPathButton=Tkinter.Button(DownloadPathFrame,text='...',command=ChooseDownloadPath)
DownloadPathButton.pack(side="left")

DownloadURLFrame=Tkinter.Frame(ControlLabelFrame)
DownloadURLFrame.pack()
DownloadURLLabel=Tkinter.Label(DownloadURLFrame,text='Download URL:',width=15)
DownloadURLLabel.pack(side="left")
DownloadURLEntry=Tkinter.Entry(DownloadURLFrame)
DownloadURLEntry.pack(side="left")
DownloadURLButton=Tkinter.Button(DownloadURLFrame,text="Paste",command=PasteURL)
DownloadURLButton.pack(side="left")

OptionsFrame=Tkinter.Frame(ControlLabelFrame)
OptionsFrame.pack()
OptionsLabel=Tkinter.Label(OptionsFrame,text="Options: ",width=12)
OptionsLabel.pack(side="left")
OptionsEntry=Tkinter.Entry(OptionsFrame)
OptionsEntry.pack(side="left")
OptionsButton=Tkinter.Button(OptionsFrame,text="...",command=ChooseOptions)
OptionsButton.pack(side="left")

ControlFrame=Tkinter.Frame(ControlLabelFrame)
ControlFrame.pack()
DownloadButton=Tkinter.Button(ControlFrame,text='Download',command=BeginDownload)
DownloadButton.pack(side="left")
OpenButton=Tkinter.Button(ControlFrame,text="Open in the finder",command=OpenDir)
OpenButton.pack(side="left")

DownloadInfoFrame=Tkinter.Frame(ControlLabelFrame)
DownloadInfoFrame.pack()
DownloadInfo=Tkinter.Text(DownloadInfoFrame,width=48)
DownloadInfo.pack(side="left",fill="y")
sl=Tkinter.Scrollbar(DownloadInfoFrame)
sl.pack(side="left",fill="y")
DownloadInfo['yscrollcommand']=sl.set
sl['command']=DownloadInfo.yview

DownloadTaskLabelFrame=Tkinter.LabelFrame(root,text="Download Task",height=100)
DownloadTaskLabelFrame.pack(side="left",fill='y')
DeletTaskButton=Tkinter.Button(DownloadTaskLabelFrame,text="Delete Task",command=DeleteTask)
DeletTaskButton.pack()
TaskFrame=Tkinter.Frame(DownloadTaskLabelFrame)
TaskFrame.pack()
DownloadArray=Tkinter.Listbox(TaskFrame,width=42,height=26)
DownloadArray.pack(side="left")
Tasksl=Tkinter.Scrollbar(TaskFrame)
Tasksl.pack(side="left",fill="y")
DownloadArray['yscrollcommand'] = Tasksl.set
Tasksl['command'] = DownloadArray.yview

root.protocol( 'WM_DELETE_WINDOW', callback)

root.mainloop()