# -*- coding: gbk -*-
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
from time import time
import threading
import mythread
import urlwork
import time
from _datetime import datetime
import inspect
import ctypes
from threading import Thread

urlwork = urlwork.MyUrl()
event_flag = threading.Event()
def getCurrentTime():  # ��ȡϵͳ��ǰʱ��
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def insertScr(str):  # ��tab1�е�scr�����������¼
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " " + str)
    scr.see(tk.END)


def loginbtn():  # tab��¼��ť
    insertScr("\n�û���:" + uname.get() + '\n����:' + pwd.get() + "\n������:" + inv.get())
    token = urlwork.getToken(uname.get(), pwd.get())
    if (token.decode("gbk") != "-2"):
        try:
            with open("account") as fp:
                tkinter.messagebox.showinfo(title='��ϲ', message='��¼�ɹ���')
                # �ѵ�¼�ɹ�����Ϣд����ʱ�ļ�
                with open(filename, 'w') as fp:
                    fp.write(','.join((uname.get(), pwd.get())))
        except:
            pass
        insertScr("��¼�ɹ�")

        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼�ɹ�")
    else:
        insertScr("��¼ʧ��")
        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼ʧ��")


def radiobuttonDo():  # tab1��ѡ��ť
    insertScr("������radiobutton " + var.get())
    if (var.get() == "d"):
        scr.delete(1.0, tkinter.END)


# ɱ���߳�
def stopTh(tid,msg, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    insertScr(msg+"�ѽ�������!")


def doWork(msg):
    # 1.��ȡtoken    if (loginbtn):
    logintoken = urlwork.getToken(uname.get(), pwd.get())
    # 2.��ȡ�ֻ���

    while 3:
        telNumber = urlwork.getTelNum(logintoken)
        insertScr(msg+"�ֻ���:" + telNumber[3:13].decode("gbk"))
        # 3.��ȡ��֤��
        verification_code = ""
        for i in range(100):
            verification_code = urlwork.getVerificationCode(logintoken, telNumber)
            if (verification_code.decode("gbk") != "-1"):
                insertScr(msg+"��֤��:" + verification_code.decode("gbk"))
                break
            else:
                insertScr(msg+"��ȡ��֤��ʧ��  " + verification_code.decode("gbk"))
                time.sleep(6)
    # 4.�ͷ��ֻ���
    n = urlwork.releaseNum(logintoken, telNumber[3:13])
    if (n.decode("gbk") == "1"):
        insertScr(msg+"�����ͷųɹ�")
    else:
        insertScr(msg+"�����ͷ�ʧ��")


def creatTh(maxNum):
    global thList
    thList=[]
    for i in range(maxNum):
        i = threading.Thread(target=doWork,name=str(i), args=("[����"+str(i)+"]",))
        thList.append(i)
    return thList


def runbtn():
    th = creatTh(thtext.get())
    for t in th:
        #t.setDaemon(True)
        t.start()


def stopbtn():
    for th in thList:
        stopTh(th.ident,"[����"+th.getName()+"]", SystemExit)


def checkEntry():
    if (uname.get().replace(" ", "") == ""):
        tkinter.messagebox.showwarning("����", "�û�������Ϊ��!")


def checkThEntry(content):
    def test(content):
        # ���������==""�Ļ����ͻᷢ��ɾ���ꡣ�ܻ�ʣ��һ������
        if content.isdigit() or content == "":
            return True
        else:
            tkinter.messagebox.showwarning("����", "�̱߳���������!")
            return False


root = tk.Tk()
root.title("����")
root.geometry('810x660')  # ��x ����*
root.resizable(width=False, height=0)  # ���ɱ�, �߲��ɱ�,Ĭ��Ϊ0
tabControl = ttk.Notebook(root, height=620, padding=0, width=800, style="BW.TLabel")
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text=" ����̨ ")
tabControl.add(tab2, text=" ��  �� ")
tabControl.add(tab3, text=" ��  �� ")
tabControl.grid(padx=4, pady=4)

style = ttk.Style()
thentrycheck = root.register(checkThEntry)
nameandpwdentrycheck = root.register(checkEntry)
style.configure("BW.TLabel", foreground="#32CD32", background="white")

var = tk.StringVar()

label_frame_loging = ttk.LabelFrame(tab1, text="��¼��", width=300, height=300)
label_frame_log = ttk.LabelFrame(tab1, text="���м�¼", width=400, height=500)
label_frame_loging.grid(row=0, column=1, padx=5, sticky=tk.N)
label_frame_log.grid(row=0, column=0, padx=5, sticky=tk.S)

radiobutton1 = ttk.Radiobutton(label_frame_loging, text="Ѷ��", variable=var, value="a", command=radiobuttonDo)
radiobutton2 = ttk.Radiobutton(label_frame_loging, text="����", variable=var, value="d", command=radiobuttonDo)
user_name = ttk.Label(label_frame_loging, text="�û���:")
password = ttk.Label(label_frame_loging, text="����:")
Invite_code = ttk.Label(label_frame_loging, text="������:")
thlabel = ttk.Label(label_frame_loging, text="�߳���:")
loginbtn = tk.Button(label_frame_loging, text="��¼", command=loginbtn)

runbutton = tk.Button(tab1, text="����", command=runbtn, width=10)
stopbutton = tk.Button(tab1, text="ֹͣ", command=stopbtn, width=10)
scr = scrolledtext.ScrolledText(label_frame_log, width=50)
scr.grid(row=0, column=0, pady=0)
uname = tk.StringVar()
uname_text = ttk.Entry(label_frame_loging, textvariable=uname, validate='focusout',
                       validatecommand=(nameandpwdentrycheck, '%P'))
pwd = tk.StringVar()
pwd_text = ttk.Entry(label_frame_loging, textvariable=pwd, validatecommand=(nameandpwdentrycheck, '%P'))
inv = tk.StringVar()
inv_text = ttk.Entry(label_frame_loging, textvariable=inv)
thtext = tk.IntVar()
thtext.set(1)
th_text = ttk.Entry(label_frame_loging, textvariable=thtext, validate='key', validatecommand=(thentrycheck, '%P'))
radiobutton1.grid(row=0, column=0)
radiobutton2.grid(row=0, column=1)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)
Invite_code.grid(row=3, padx=2, pady=3)
inv_text.grid(row=3, column=1, padx=2, pady=3)
thlabel.grid(row=4, column=0)
th_text.grid(row=4, column=1)

loginbtn.grid(row=5, ipadx=20)

runbutton.grid(row=0, column=1, padx=5, sticky=tk.S)
stopbutton.grid(row=0, column=1, padx=5, sticky=tk.S + tk.E)
try:
    with open("account") as fp:
        n, p = fp.read().strip().split(',')
        uname.set(n)
        pwd.set(p)
except:
    pass
root.mainloop()
