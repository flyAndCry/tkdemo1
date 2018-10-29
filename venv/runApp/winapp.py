# -*- coding: gbk -*-
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
from time import time
import urllib.parse
import urllib.request
import  threading
import mythread

import time
from _datetime import datetime


class WinApp(object):
    def __init__(self):
        a = 1


def getCurrentTime():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def loginbtn():
    scr.insert(tk.INSERT,
               getCurrentTime() + "\n" + "�û���:" + uname.get() + '\n' + "����:" + pwd.get() + "\n" + "������:" + inv.get() + "\n")
    token = getToken()
    if (token != -2):
        scr.insert(tk.INSERT, getCurrentTime() + " \n��¼�ɹ� token:" + token.decode("gbk"))
        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼�ɹ�")
    else:
        scr.insert(tk.INSERT, getCurrentTime() + "��¼ʧ��" + token.decode("gbk"))
        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼ʧ��")
    return token


def getResponse(url, data):
    params = urllib.parse.urlencode(data)
    url = url % params
    with urllib.request.urlopen(url, timeout=100) as response:
        return response.read()


def getTelNum(token):
    data = {
        "token": token,
        "xmid": 200,
        "sl": 1,
        "lx": 1,
        "a1": "",
        "a2": "",
        "pk": "",
        "ks": 0,
        "rj": 0
    }
    url = 'http://47.106.71.60:9180/service.asmx/GetHM2Str?%s'
    return getResponse(url, data)


def getVerificationCode(token, telNumber):
    url = "http://47.106.71.60:9180/service.asmx/GetYzm2Str?%s"
    data = {
        "token": token,
        "hm": telNumber[3:13],
        "xmid": 200,
        "sf": 0
    }
    return getResponse(url, data)


def getToken():
    data = {
        "name": uname.get(),
        "psw": pwd.get()
    }
    url = "http://47.106.71.60:9180/service.asmx/UserLoginStr?%s"
    return getResponse(url, data)


def radiobuttonDo():
    scr.insert(tk.INSERT, "\n" + " ������radiobutton    " + var.get())
    if (var.get() == "d"):
        scr.delete(1.0, tkinter.END)


def doWork(msg):
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + msg)
    stopbutton["background"] = "#F5F5F5"  # �׻�
    runbutton["background"] = "SpringGreen"  # ������
    # 1.��ȡtoken    if (loginbtn):
    logintoken = getToken()
    # 2.��ȡ�ֻ���
    telNumber = getTelNum(logintoken)
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " �ֻ���:" + telNumber[3:13].decode("gbk"))
    # 3.��ȡ��֤��
    while 1:
        verification_code = getVerificationCode(logintoken, telNumber)
        if (verification_code.decode("gbk") != "-1"):
            scr.insert(tk.INSERT, "\n" + getCurrentTime() + " ��֤��:" + verification_code.decode("gbk"))
            break
        else:
            scr.insert(tk.INSERT, "\n" + getCurrentTime() + " ��ȡ��֤��ʧ��  " + verification_code.decode("gbk"))
            time.sleep(6)

    # 4.�ͷ��ֻ���


def runbtn():
    runbutton["background"] = "#008000"  # ����
    stopbutton["background"] = "#F5F5F5"  # ���Ѻ�
    th = threading.Thread(target=doWork, args=("\n" + " ��ʼ����.....",))
    th.setDaemon(True)  # �ػ��߳�
    th.start()
    # th = mythread.Th(target=doWork, args=("\n" + " ��ʼ����.....",))
    # th.setDaemon(True)  # �ػ��߳�
    # th.start()


def stopbtn():
    runbutton["background"] = "#F5F5F5"  # �׻�
    stopbutton["background"] = "#FF6347"  # ���Ѻ�


def checkEntry():
    if (uname.get().replace(" ", "") == ""):
        tkinter.messagebox.showwarning("����", "�û�������Ϊ��!")



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
loginbtn = tk.Button(label_frame_loging, text="��¼", command=loginbtn)
runbutton = tk.Button(tab1, text="����", command=runbtn, width=10)
stopbutton = tk.Button(tab1, text="ֹͣ", command=stopbtn, width=10)
scr = scrolledtext.ScrolledText(label_frame_log, width=50)
scr.grid(row=0, column=0, pady=0)
uname = tk.StringVar()
uname_text = ttk.Entry(label_frame_loging, textvariable=uname, validate='focusout', validatecommand=checkEntry)
pwd = tk.StringVar()
pwd_text = ttk.Entry(label_frame_loging, textvariable=pwd)
inv = tk.StringVar()
inv_text = ttk.Entry(label_frame_loging, textvariable=inv)
radiobutton1.grid(row=0, column=0)
radiobutton2.grid(row=0, column=1)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)
Invite_code.grid(row=3, padx=2, pady=3)
inv_text.grid(row=3, column=1, padx=2, pady=3)
loginbtn.grid(row=4, ipadx=20)

runbutton.grid(row=0, column=1, padx=5, sticky=tk.S)
stopbutton.grid(row=0, column=1, padx=5, sticky=tk.S + tk.E)

root.mainloop()
