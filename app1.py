from mega import Mega
from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import shutil,os,speedtest,os.path,time

login="" #сюда почту с которой залогинился в мегу
password="" #сюда пароль от акка меги

g=" "
# Function for opening the 
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    global g
    g=filename
    lbl3.configure(text=filename)
      

#--------speedtest staff--------
#s = speedtest.Speedtest()

def bytesto(bytes, bsize=1024):
    r = float(bytes)
    for i in range(2):
        r = r / bsize

    return(r)

#------Mega staff---------
foldername=""
mega = Mega()
m = mega.login(login,password) #логинюсь
#some functions
def checkisdirorfile(g):
    if os.path.isfile(g):
        return uploadfile(g,foldername)
    if os.path.isdir(g):
        return archivefile(foldername,g)

def archivefile(foldername,g):
    filename=g
    shutil.make_archive(filename,'zip',root_dir=g)
    return uploadfile(filename+'.zip',foldername)

def uploadfile(x,folder):
    if (len(folder)!=0):
        file = m.upload(x,folder[0]) 
    else:
        file = m.upload(x)
    z=m.get_upload_link(file)
    if x.__contains__("zip"):
        os.remove(x)
    return z

#-------Gui staff---------
root = Tk() 
Checkbutton1 = IntVar()
style = Style()
root.title("Upload to mega") 
root.geometry('425x200')
root.minsize(425, 230) 
root.config(background = "white")
#Style
style.configure('TButton', font =
               ('calibri', 10, 'bold'),
                foreground = 'blue',background='black')
style.configure("BW.TLabel", background="white")
#---------text inside window---------
#folder in which upload
lbl = Label(root, text = "In which folder upload",style="BW.TLabel")
lbl.grid(column=0,row=0)


lbl1 = Label(root, text = "",style="BW.TLabel")
lbl1.grid(column=1,row=0)

#folder which upload

lbl2 = Label(root, text = "Folder or file to upload:",style="BW.TLabel")
lbl2.grid(column=0,row=3)

lbl3 = Label(root, text = "",style="BW.TLabel")
lbl3.grid(column=0,row=4)

lbl4 = Label(root, text = "",style="BW.TLabel")
lbl4.grid(column=0,row=10)

lbl5 = Label(root, text = "",style="BW.TLabel")
lbl5.grid(column=1,row=8)

lbl6 = Label(root, text = "",style="BW.TLabel")
lbl6.grid(column=1,row=6)
#---------entry field---------
# adding Entry Field
txt = Entry(root, width=50)
txt.grid(column=0, row =1)
#------------buttons--------------
 
#function on 1 button click
def foldernamechecker():
    if m.find(str(txt.get())):
        global foldername
        foldername = m.find(str(txt.get()))
        res = "Folder exists!"
    else:
        res = "Folder not exists!"
    lbl1.configure(text = res)

#function on upload button
def upfile():
    Megas=checkisdirorfile(g)
    root.clipboard_clear()
    root.clipboard_append(Megas)
    root.update()
    messagebox.showinfo("showinfo", "link was saved to clipboard!") 

#space left
def knowstrspc():
    res=str(m.get_storage_space(giga=True))
    xex= res[9:14]
    xec=res[36:39]
    left= float(xec)-float(xex)
    lbl5.configure(text = "total:"+xec+"\nused:"+xex+"\nleft:"+str(left))

def speddtest():
    xex = bytesto(s.download())
    xec = bytesto(s.upload())
    while xex is None or xec is None:
        timer=timer+1
        time.sleep(1)
        lbl6.configure(text="Time elapsed:"+str(timer)) 
    lbl4.configure(text="download speed:"+str(xex)[:5]+" Mbps"+"\nupload speed:"+str(xec)[:5]+" Mbps")
#button
btn = Button(root, text = "Submit!" ,
             style = 'TButton', command=foldernamechecker)
btn.grid(column=1, row=1,padx = 10)

#button2
btn1 = Button(root, text = "explore files" ,
             style = 'TButton', command=browseFiles)
btn1.grid(column=1, row=4,padx = 10)
#button to upload
btn2 = Button(root, text = "Start!" ,
             style = 'TButton', command=upfile)
btn2.grid(column=0, row=7,padx = 0)
#buuton 3
btn2 = Button(root, text = "Space left" ,
             style = 'TButton', command=knowstrspc)
btn2.grid(column=1, row=7,padx = 0)
#button 4
btn3 = Button(root, text = "Speedtest!" ,
             style = 'TButton', command=speddtest)
btn3.grid(column=0, row=8,padx = 0)
#adding check button

root.mainloop()