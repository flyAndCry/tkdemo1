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
import  mytable
mytab=mytable.Mytable()
urlwork = urlwork.MyUrl()
event_flag = threading.Event()

thList = []
massageToken=None

def getCurrentTime():  # ��ȡϵͳ��ǰʱ��
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def insertScr(str):  # ��tab1�е�scr�����������¼
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " " + str)
    scr.see(tk.END)


def loginbtn():  # tab��¼��ť
    insertScr("\n�û���:" + uname.get() + '\n����:' + pwd.get() + "\n������:" + inv.get())
    global  massageToken
    massageToken = urlwork.getToken(uname.get(), pwd.get())
    if (massageToken.decode("gbk") != "-2"):
        try:
            with open("account") as fp:
                #tkinter.messagebox.showinfo(title='��ϲ', message='��¼�ɹ���')
                # �ѵ�¼�ɹ�����Ϣд����ʱ�ļ�
                with open(filename, 'w') as fp:
                    fp.write(','.join((uname.get(), pwd.get())))
        except:
            pass
        insertScr("��¼�ɹ�")

        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼�ɹ�")
    else:
        insertScr("��¼ʧ��")
        massageToken=None
        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼ʧ��")


def radiobuttonDo():  # tab1��ѡ��ť
    insertScr("������radiobutton " + var.get())
    if (var.get() == "d"):
        scr.delete(1.0, tkinter.END)


# ɱ���߳�
def stopTh(tid, msg, exctype):
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
    insertScr(msg + "�ѽ�������!")


def doWork(msg):
    insertScr(msg+"is running...")
    while 3:
        # 1.��ȡtoken    if (loginbtn):
        if massageToken is None:
            tkinter.messagebox.showinfo(title='��ʾ', message='���¼��')
        else:
            logintoken=massageToken
        # 2.��ȡ�ֻ���

        telNumber = urlwork.getTelNum(logintoken)
        insertScr(msg + "�ֻ���:" + telNumber[3:13].decode("gbk"))
        # 3.��ȡ��֤��
        verification_code = ""
        for i in range(1):
            verification_code = urlwork.getVerificationCode(logintoken, telNumber)
            if (verification_code.decode("gbk") != "-1"):
                insertScr(msg + "��֤��:" + verification_code.decode("gbk"))
                break
            else:
                insertScr(msg + "��ȡ��֤��ʧ��  " + verification_code.decode("gbk"))
                time.sleep(6)
        # 4.�ͷ��ֻ���
        n = urlwork.releaseNum(logintoken, telNumber[3:13])
        if (n.decode("gbk") == "1"):
            insertScr(msg + "�����ͷųɹ�")
        else:
            insertScr(msg + "�����ͷ�ʧ��")
        tree.insert("", "end", values=(i + 1,telNumber[3:13],"123456789","OK","-"))

def creatTh(maxNum):
    global thList
    thList=[]
    for i in range(maxNum):
        i = threading.Thread(target=doWork, name=str(i), args=("[����" + str(i) + "]",))
        thList.append(i)
    return thList


def runbtn():
    th = creatTh(thtext.get())
    for t in th:
        # t.setDaemon(True)
        t.start()


def stopbtn():
    for th in thList:
        stopTh(th.ident, "[����" + th.getName() + "]", SystemExit)

def testbtn():
    insertScr("���Գɹ�!!")

def dailbtn():
    insertScr("���Ų��Գɹ�!")
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
root.iconbitmap("bitbug_favicon.ico")
root.geometry('810x660')  # ��x ����*
root.resizable(width=False, height=0)  # ���ɱ�, �߲��ɱ�,Ĭ��Ϊ0
tabControl = ttk.Notebook(root, height=620, padding=0, width=825, style="BW.TLabel")
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text=" ����̨ ")
tabControl.add(tab2, text=" ��  �� ")
tabControl.add(tab3, text=" ��  �� ")
tabControl.grid(padx=4, pady=4)
#-------------------------------------------------------tab1---------------------------------------------------------
style = ttk.Style()
thentrycheck = root.register(checkThEntry)
nameandpwdentrycheck = root.register(checkEntry)
style.configure("BW.TLabel", foreground="#32CD32", background="white")

var = tk.StringVar()

label_frame_log = ttk.LabelFrame(tab1, text="���м�¼", width=400, height=400)
controlled_center_frame = ttk.LabelFrame(tab1, text="��������", width=400, height=280)
controlled_center_bottom_frame = ttk.LabelFrame(controlled_center_frame, text="������", width=390, height=300)
controller_center_head_frame = ttk.LabelFrame(controlled_center_frame, text="����", width=390, height=300)
controller_center_center_frame = ttk.LabelFrame(controlled_center_frame, text="��IP", width=390, height=300)
controller_center_center_inside_frame = ttk.LabelFrame(controller_center_center_frame, text="���ʴ���", width=390, height=300)
dial_frame = ttk.LabelFrame(controller_center_center_frame, text="����", width=390, height=300)

controller_center_head_frame.grid(row=0, padx=5, sticky=tk.N + tk.W + tk.E)
controlled_center_frame.grid(row=0, column=1, padx=5, sticky=tk.N)
label_frame_log.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S)
controlled_center_bottom_frame.grid(row=2, padx=5)
controller_center_center_frame.grid(row=1,padx=5)
controller_center_center_inside_frame.grid(row=1,column=0)
dial_frame.grid(row=1,column=1)
radiobutton1 = ttk.Radiobutton(controller_center_head_frame, text="Ѷ��", variable=var, value="a", command=radiobuttonDo)
radiobutton2 = ttk.Radiobutton(controller_center_head_frame, text="����", variable=var, value="b", command=radiobuttonDo)
radiobutton3 = ttk.Radiobutton(controller_center_head_frame, text="����", variable=var, value="c", command=radiobuttonDo)
# radiobutton4 = ttk.Radiobutton(controller_center_head_frame , text="��", variable=var, value="c", command=radiobuttonDo)
radiobutton5 = ttk.Radiobutton(controller_center_center_frame , text="����", variable=var, value="d", command=radiobuttonDo)
radiobutton6 = ttk.Radiobutton(controller_center_center_frame , text="Ѷ����", variable=var, value="e", command=radiobuttonDo)
#radiobutton7 = ttk.Radiobutton(controller_center_center_frame , text="����ip", variable=var, value="f", command=radiobuttonDo)
user_name = ttk.Label(controller_center_head_frame, text="�û���:")
password = ttk.Label(controller_center_head_frame, text="��   ��:")
Invite_code = ttk.Label(controlled_center_bottom_frame, text="������:")
loginbtn = tk.Button(controller_center_head_frame, text="��¼", command=loginbtn)

thlabel = ttk.Label(controlled_center_bottom_frame, text="�߳���:")
ctrlabel = ttk.Label(controlled_center_bottom_frame, text="������:")

diallabel = ttk.Label(controlled_center_bottom_frame, text="�����ӳ�:")
randomPWDcheck= ttk.Checkbutton(controlled_center_bottom_frame, text="�������")
fixedpwdlab = ttk.Label(controlled_center_bottom_frame, text="�̶�����:")
spiderIdlab = ttk.Label(controller_center_center_inside_frame, text="spiderId:")
orderlab = ttk.Label(controller_center_center_inside_frame, text="������:")
iplabel = ttk.Label(controller_center_center_inside_frame, text="ʹ�ô���:")
BWaccountlabel = ttk.Label(dial_frame, text="����˺�:")
BWpwdlabel = ttk.Label(dial_frame, text="�������:")
filterIPcheck= ttk.Checkbutton(dial_frame, text="������ͬIP")
runbutton = tk.Button(controlled_center_bottom_frame, text="����", command=runbtn, width=10)
stopbutton = tk.Button(controlled_center_bottom_frame, text="ֹͣ", command=stopbtn, width=10)
testbutton = tk.Button(controller_center_center_inside_frame, text="����", command=testbtn, width=10)
dialbutton = tk.Button(dial_frame, text="���Ų���", command=dailbtn, width=10)
scr = scrolledtext.ScrolledText(label_frame_log, width=50,height=50)
scr.grid(row=0, column=0, pady=0)
uname = tk.StringVar()
uname_text = ttk.Entry(controller_center_head_frame, textvariable=uname, validate='focusout',
                       validatecommand=(nameandpwdentrycheck, '%P'))
pwd = tk.StringVar()
pwd_text = ttk.Entry(controller_center_head_frame, textvariable=pwd, validatecommand=(nameandpwdentrycheck, '%P'))
inv = tk.StringVar()
inv_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=inv)
thtext = tk.IntVar()
thtext.set(1)
th_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=thtext, validate='key',
                    validatecommand=(thentrycheck, '%P'))
ctrtext = tk.IntVar()
ctrtext.set(1)
ctr_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=ctrtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))

ip_comboxlisttext=tkinter.StringVar()#�����Դ����ı����½�һ��ֵ
ip_comboxlist_text = ttk.Combobox(controller_center_center_inside_frame,width=10, textvariable=ip_comboxlisttext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
ip_comboxlist_text["values"]=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
dialtext = tk.IntVar()
dialtext.set(1)
dial_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=dialtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
fixedpwd = tk.IntVar()
fixedpwd.set(1)
fixedpwd_text = ttk.Entry(controlled_center_bottom_frame,width=10, textvariable=fixedpwd, validate='key',
                     validatecommand=(thentrycheck, '%P'))
spiderIdtext = tk.StringVar()
spiderId_text = ttk.Entry(controller_center_center_inside_frame,width=15, textvariable=spiderIdtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
ordertext = tk.StringVar()
order_text = ttk.Entry(controller_center_center_inside_frame,width=15, textvariable=ordertext, validate='key',
                     validatecommand=(thentrycheck, '%P'))

BWaccounttext = tk.StringVar()
BWaccount_text = ttk.Entry(dial_frame,width=15, textvariable=BWaccounttext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
BWpwdtext = tk.StringVar()
BWpwd_text = ttk.Entry(dial_frame,width=15, textvariable=BWpwdtext, validate='key',
                     validatecommand=(thentrycheck, '%P'))
radiobutton1.grid(row=0, column=0, padx=5)
radiobutton2.grid(row=0, column=1, padx=5)
radiobutton3.grid(row=0, column=2, padx=5)
# radiobutton4.grid(row=0,column=3,padx=5,sticky=tk.E)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)

thlabel.grid(row=0, column=2, padx=2, pady=3)
th_text.grid(row=0, column=3, padx=2, pady=3)
ctrlabel.grid(row=0, column=0, padx=2, pady=3)
ctr_text.grid(row=0, column=1, padx=2, pady=3)

diallabel.grid(row=1,column=2,padx=2,pady=3)
randomPWDcheck.grid(row=2,column=0,padx=2,pady=3)
fixedpwdlab.grid(row=2,column=2,padx=5,pady=3)
fixedpwd_text.grid(row=2,column=3,padx=2,pady=3)
dial_text.grid(row=1,column=3,padx=2,pady=3)
Invite_code.grid(row=4, column=0,padx=2, pady=3)
inv_text.grid(row=4, column=1, padx=2, pady=3)

radiobutton5.grid(row=0,column=1,padx=2,pady=3)
radiobutton6.grid(row=0,column=0,padx=2,pady=3)
#radiobutton7.grid(row=0,column=2,padx=2,pady=3)
spiderIdlab.grid(row=1,column=0,padx=2,pady=3)
spiderId_text.grid(row=1,column=1,padx=2,pady=3)
orderlab.grid(row=2,column=0,padx=2,pady=3)
order_text.grid(row=2,column=1,padx=2,pady=3)
iplabel.grid(row=3,column=0,padx=2,pady=3)
ip_comboxlist_text.grid(row=3,column=1,padx=2,pady=3)
testbutton.grid(row=4,column=0,padx=2,pady=3,sticky=tk.S)

BWaccountlabel.grid(row=0,column=0,padx=2,pady=3)
BWaccount_text.grid(row=0,column=1,padx=2,pady=3)
BWpwdlabel.grid(row=1,column=0,padx=2,pady=3)
BWpwd_text.grid(row=1,column=1,padx=2,pady=3)
filterIPcheck.grid(row=2,column=0,padx=3,pady=3)
dialbutton.grid(row=3,column=0,padx=2,pady=3)

loginbtn.grid(row=5, ipadx=20, padx=2, pady=3)
runbutton.grid(row=6, column=0, padx=5, sticky=tk.S)
stopbutton.grid(row=6, column=1, padx=5, sticky=tk.S + tk.E)
try:
    with open("account") as fp:
        n, p = fp.read().strip().split(',')
        uname.set(n)
        pwd.set(p)
except:
    pass
#-----------------------------------------------tab3---------------------------------------------------
# ���������б�����

vbar = tkinter.Scrollbar(tab2)
tree = ttk.Treeview(tab2, show="headings", height=18, columns=("a", "b", "c", "d", "e"),yscrollcommand=vbar.set)
# ���ÿ�еĿ�ȺͶ���
tree.column("a", width=50, anchor="center")
tree.column("b", width=200, anchor="center")
tree.column("c", width=200, anchor="center")
tree.column("d", width=100, anchor="center")
tree.column("e", width=150, anchor="center")
# ���ı���
tree.heading("a", text="���")
tree.heading("b", text="�˺�")
tree.heading("c", text="����")
tree.heading("d", text="״̬")
tree.heading("e", text="��ע��Ϣ")
tree.grid(row=0, column=0)
vbar.grid(row=0, column=1)
tree.grid()

root.mainloop()
