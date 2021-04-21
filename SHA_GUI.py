import os
from tkinter import*
import tkinter.filedialog
import sha2_gui
from sha2_gui import *


"""
#print(tkinter.TkVersion)

root = Tk()
#Title
root.title("SHA_GUI_M0729017")
#size & local
#root.geometry("800x600+100+100")

#Label
#fg:word color/bg:word background color/anchor:direction/wraplength:換行/font:字型/justify:靠左靠右
lb = Label(root,bitmap="hourglass",compound="left",text="  Plz Input Data:",fg = "black",anchor="nw",font="helvetica 15",relief="raised",padx=5,pady=10)
lb.pack()        #包裝與定位元件
print(type(lb))  #傳回Label物件


#Label
#fg:word color/bg:word background color/anchor:direction/wraplength:換行/font:字型/justify:靠左靠右

label = Label(root,text="I like tkinter,I like tkinter,I like tkinter",fg = "black",bg = "yellow",anchor="se",font="helvetica 10 bold",
wraplength=80,justify="center")
label.pack()        #包裝與定位元件
print(type(label))  #傳回Label物件

label_1 = Label(root,bitmap="hourglass")
label_1.pack()


#Background
root.configure(bg='white')
root.mainloop()

"""
def ChooseFile():
    global plain
    filename=tkinter.filedialog.askopenfilename()
    plain=open(filename,mode='rb').read()

    if filename != '':
        FN.set(filename)
        PN.set(plain)
        text.insert(END,plain)
    else:
        FN.set('')
        PN.set('')

def SHA224():
    SHA=sha224.SHA224(plain).hexdigest()
    if SHA !='':
        CN_224.set(SHA)
    else:
        CN_224.set('')
def SHA256():
    SHA=sha256.SHA256(plain).hexdigest()
    if SHA !='':
        CN_256.set(SHA)
    else:
        CN_256.set('')
def SHA384():
    SHA=sha384.SHA384(plain).hexdigest()
    if SHA !='':
        CN_384.set(SHA)
    else:
        CN_384.set('')       

def SHA512():
    SHA=sha512.SHA512(plain).hexdigest()
    if SHA !='':
        CN_512.set(SHA)
    else:
        CN_512.set('')


window = Tk()
window.title("SHA2_GUI")
window.geometry("1024x768")
FN=StringVar()
PN=StringVar()
CN_224=StringVar()
CN_256=StringVar()
CN_384=StringVar()
CN_512=StringVar()

#label_1.pack()
lb_1=Label(bg="#323232",fg="white",text="Please choose the file.")
lb_1.pack(anchor=NW)

#Filename.pack()
Fname=Entry(bd =5,width=50,textvariable=FN)
Fname.pack(anchor=NW)

#btn.pack()
btn_1=Button(text="Choose",command=ChooseFile)
btn_1.pack(anchor=NW)

lb_1.pack(side=TOP)
Fname.pack(side=TOP)
btn_1.pack(side=TOP)



#label_2.pack()
lb_2=Label(text="Ciphertext")
lb_2.pack(anchor=N)
#Text
ysb = Scrollbar(window)
text = Text(window,height=20,width=100,bg="#A9A9A9")
ysb.pack(side=RIGHT,fill=Y)
text.pack()
ysb.config(command=text.yview)
text.config(yscrollcommand=ysb.set)
text.pack(anchor=N)


#btn_2.pack()
btn_2=Button(text="SHA224",command=SHA224)
btn_2.pack(anchor=NW)
#btn_2.pack()
btn_2=Button(text="SHA256",command=SHA256)
btn_2.pack(anchor=NW)
#btn_2.pack()
btn_2=Button(text="SHA384",command=SHA384)
btn_2.pack(anchor=NW)
#btn_2.pack()
btn_2=Button(text="SHA512",command=SHA512)
btn_2.pack(anchor=NW)
#Filename.pack()
Fname_1=Entry(bd =5,width=200,textvariable=CN_224)
Fname_1.pack(anchor=NW)
#Filename.pack()
Fname_2=Entry(bd =5,width=200,textvariable=CN_256)
Fname_2.pack(anchor=NW)
#Filename.pack()
Fname_3=Entry(bd =5,width=200,textvariable=CN_384)
Fname_3.pack(anchor=NW)
#Filename.pack()
Fname_4=Entry(bd =5,width=200,textvariable=CN_512)
Fname_4.pack(anchor=NW)






window.mainloop()