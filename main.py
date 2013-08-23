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
def DownloadProcess(DownloadURL,DownloadPath,DownloadOptions):
    if DownloadURL[0:4]!="http" and DownloadURL[0:5]!="https":
        tkMessageBox.showwarning("Wrong URL","%s is not a correct URL (include http or https)" \
                                             %DownloadURL)
    else:
        P=subprocess.Popen("%s --newline %s %s -o '%s"%(DownloadProgram,DownloadOptions,DownloadURL,DownloadPath)+"%(title)s.%(ext)s'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        DownloadInfo.delete(1.0,"end")
        DownloadButton['state']='disable'
        tmp=P.stdout.readline()
        while tmp!='':
            DownloadInfo.insert(1.0,"%s\n"%tmp)
            if P.stdout.readline().find("Error")>=0 or P.stdout.readline().find("error")>=0 or P.stdout.readline().find("ERROR")>=0:
                tkMessageBox.showwarning("Downlad Fail","There is something wrong. Please double check inputs.")
                break
            else:
                tmp=P.stdout.readline()
        DownloadInfo.insert(1.0,"%s\n"%"Finish!!")
        DownloadButton['state']='normal'
#开始下载
def BeginDownload():
    DownloadPath=DownloadPathEntry.get()
    DownloadURL=DownloadURLEntry.get()
    DownloadOptions=OptionsEntry.get()
    if os.path.exists(DownloadPath):
        t=threading.Thread(target=DownloadProcess,args=(DownloadURL,DownloadPath,DownloadOptions))
        t.start()
    else:
        if tkMessageBox.askquestion("Wrong Path",\
                                 "There isn't %s. Would you like to create it?"%DownloadPath)=='yes':
            try:
                os.makedirs(DownloadPath)
                t=threading.Thread(target=DownloadProcess,args=(DownloadURL,DownloadPath,DownloadOptions))
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
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--playlist-end NUMBER ":
            try:
                i="--playlist-end %s "%tkSimpleDialog.askinteger("Playlist End","What is the playlist end number?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--match-title REGEX ":
            try:
                i="--match-title %s "%tkSimpleDialog.askstring("Title","What is the match title?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--reject-title REGEX ":
            try:
                i="--reject-title %s "%tkSimpleDialog.askstring("Title","What is the reject title?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--max-downloads NUMBER ":
            try:
                i="--max-downloads %s "%tkSimpleDialog.askinteger("Max Downloads","What is the maximum download number?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--min-filesize SIZE ":
            try:
                i="--min-filesize %s "%tkSimpleDialog.askstring("Minimum file size", "What is the minimum file size?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--max-filesize SIZE ":
            try:
                i="--max-filesize %s "%tkSimpleDialog.askinteger("Maximum file size","What is the maximum file size?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--date DATE ":
            try:
                i="--date %s "%tkSimpleDialog.askstring("Video Upload Date","What is the date in which you want to download video?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--datebefore DATE ":
            try:
                i="--datebefore %s "%tkSimpleDialog.askstring("Video Upload Data","What is the date before which you want to download video?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--dateafter DATE ":
            try:
                i="--dateafter %s "%tkSimpleDialog.askstring("Video Upload Data","What is the date after which you want to download video?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="-r LIMIT ":
            try:
                i="-r %s "%tkSimpleDialog.askstring("Maximum speed","Waht is the maximum download speed?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="-R RETRIES ":
            try:
                i="-R %s "%tkSimpleDialog.askstring("Maximum number of retries","What is the maximum number of retries?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--buffer-size SIZE ":
            try:
                i="--buffer-size %s "%tkSimpleDialog.askstring("Maximum buffer size","What is the maximum buffer size?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--sub-lang LANG ":
            try:
                i="--sub-lang %s "%tkSimpleDialog.askstring("Language","what is the language that you want to download?")
                OptionsEntry.insert('end',i)
            except:
                continue
        elif Options[int(i)][0:Options[int(i)].find("    ")+1]=="--audio-quality QUALITY ":
            try:
                i="--audio-quality %s "%tkSimpleDialog.askinteger("Quality","What is the Quality that you want to download?")
                OptionsEntry.insert('end',i)
            except:
                continue
        else:
            OptionsEntry.insert('end',Options[int(i)][0:Options[int(i)].find("    ")+1])
    ChooseOptionsWindow.destroy()
########################################################################



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

OptionsFrame=Tkinter.Frame(root)
OptionsFrame.pack()
OptionsLabel=Tkinter.Label(OptionsFrame,text="Options: ",width=12)
OptionsLabel.pack(side="left")
OptionsEntry=Tkinter.Entry(OptionsFrame)
OptionsEntry.pack(side="left")
OptionsButton=Tkinter.Button(OptionsFrame,text="...",command=ChooseOptions)
OptionsButton.pack(side="left")

ControlFrame=Tkinter.Frame(root)
ControlFrame.pack()
DownloadButton=Tkinter.Button(ControlFrame,text='Download',command=BeginDownload)
DownloadButton.pack(side="left")
OpenButton=Tkinter.Button(ControlFrame,text="Open in the finder",command=OpenDir)
OpenButton.pack(side="left")

DownloadInfoFrame=Tkinter.Frame(root)
DownloadInfoFrame.pack()
DownloadInfo=Tkinter.Text(DownloadInfoFrame,width=48)
DownloadInfo.pack(side="left",fill="y")
sl=Tkinter.Scrollbar(DownloadInfoFrame)
sl.pack(side="left",fill="y")
DownloadInfo['yscrollcommand']=sl.set
sl['command']=DownloadInfo.yview

#DownloadArrayFrame=Tkinter.Frame(root)
#DownloadArrayFrame.pack()
#DownloadArray=Tkinter.Listbox(DownloadArrayFrame,width=42)
#DownloadArray.pack(side="left")
#sl=Tkinter.Scrollbar(DownloadArrayFrame)
#sl.pack(side="left",fill="y")
#DownloadArray['yscrollcommand'] = sl.set
#sl['command'] = DownloadArray.yview

root.mainloop()