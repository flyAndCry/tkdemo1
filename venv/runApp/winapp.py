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
import mytable

mytab = mytable.Mytable()
urlwork = urlwork.MyUrl()
event_flag = threading.Event()

thList = []
massageToken = None


class win(object):
    def __init__(self):
        a = 1

    def ttt(self, tab3):
        ttvar = tk.StringVar()
        tt = ttk.Label(tab3, text="����label", textvariable=ttvar)
        teER = ttk.Entry(tt, width=20)
        tt.grid()
        teER.grid()


def getCurrentTime():  # ��ȡϵͳ��ǰʱ��
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def insertScr(str):  # ��tab1�е�scr�����������¼
    scr.insert(tk.INSERT, "\n" + getCurrentTime() + " " + str)
    scr.see(tk.END)


def loginbtn():  # tab��¼��ť
    insertScr("\n�û���:" + uname.get() + '\n����:' + pwd.get())
    global massageToken
    massageToken = urlwork.getToken(uname.get(), pwd.get())
    if (massageToken.decode("gbk") != "-2"):
        try:
            with open("account") as fp:
                # tkinter.messagebox.showinfo(title='��ϲ', message='��¼�ɹ���')
                # �ѵ�¼�ɹ�����Ϣд����ʱ�ļ�
                with open(filename, 'w') as fp:
                    fp.write(','.join((uname.get(), pwd.get())))
        except:
            pass
        insertScr("��¼�ɹ�")

        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼�ɹ�")
    else:
        insertScr("��¼ʧ��")
        massageToken = None
        # tkinter.messagebox.showinfo(title="��ʾ", message="��¼ʧ��")


def radiobuttonDo():  # tab1��ѡ��ť
    #urlwork.testSrc(tk.INSERT, scr)
    urlwork.testFrame()


def clearRunninglogButton():
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
    insertScr(msg + "is running...")

    while 3:
        # 1.��ȡtoken    if (loginbtn):
        if massageToken is None:
            tkinter.messagebox.showinfo(title='��ʾ', message='���¼���Ž���ƽ̨��')
            break
        else:
            logintoken = massageToken
            currentIp_var.set("192.168.0.0")
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
        tree.insert("", "end", values=(i + 1, telNumber[3:13], "123456789", "OK", "-"))


def creatTh(maxNum):
    global thList
    thList = []
    for i in range(maxNum):
        i = threading.Thread(target=doWork, name=str(i), args=("[����" + str(i) + "]",))
        thList.append(i)
    return thList


def runbtn():
    th = creatTh(thread_count_var.get())
    for t in th:
        t.setDaemon(True)
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


def closeRootWinAsk():
    askokcancel = tk.messagebox.askokcancel("��ʾ", "�رմ��ڽ��˳�����!")
    if askokcancel:
        root.destroy()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", closeRootWinAsk)
root.title("����")
root.iconbitmap("bitbug_favicon.ico")


def center_window(w, h):
    # ��ȡ��Ļ ����
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # ���� x, y λ��
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


center_window(810, 660)
root.resizable(width=False, height=0)  # ���ɱ�, �߲��ɱ�,Ĭ��Ϊ0
tabControl = ttk.Notebook(root, height=620, padding=0, width=825)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text=" ����̨ ")
tabControl.add(tab2, text=" ��  �� ")
tabControl.add(tab3, text=" ��  �� ")
tabControl.grid(padx=4, pady=4)
# -------------------------------------------------------tab1---------------------------------------------------------
style = ttk.Style()
style.configure("BW.TLabel", foreground="#556B2F", background="#556B2F")
thentrycheck = root.register(checkThEntry)
nameandpwdentrycheck = root.register(checkEntry)
# configure = ttk.Style().configure(".", font=("����", 25))
var = tk.StringVar()
runninglog_lableframe = ttk.LabelFrame(tab1, text="���м�¼", width=400, height=300)
scr = scrolledtext.ScrolledText(runninglog_lableframe, width=50, height=36.3, fg="blue")
currentIpLab = ttk.Label(runninglog_lableframe, text="      �� ǰ IP:")
currentIp_var = tk.StringVar()
currentIp_text = ttk.Entry(runninglog_lableframe, textvariable=currentIp_var, width=30)
scr.grid(row=0, pady=0)
currentIpLab.grid(row=1, sticky=tk.S + tk.W)
currentIp_text.grid(row=1, sticky=tk.S)

controllercenter_lableframe = ttk.LabelFrame(tab1, text="��������", width=400, height=280)
massage_lableframe = ttk.LabelFrame(controllercenter_lableframe, text="����", width=390, height=300)
radiobutton1 = ttk.Radiobutton(massage_lableframe, text="Ѷ��", variable=var, value="a", command=radiobuttonDo)
radiobutton2 = ttk.Radiobutton(massage_lableframe, text="����", variable=var, value="b", command=radiobuttonDo)
radiobutton3 = ttk.Radiobutton(massage_lableframe, text="����", variable=var, value="c", command=radiobuttonDo)
radiobutton1.grid(row=0, column=0, padx=5)
radiobutton2.grid(row=0, column=1, padx=5)
radiobutton3.grid(row=0, column=2, padx=5)
user_name = ttk.Label(massage_lableframe, text="�û���:")
uname = tk.StringVar()
uname_text = ttk.Entry(massage_lableframe, textvariable=uname, validate='focusout',
                       validatecommand=(nameandpwdentrycheck, '%P'))
password = ttk.Label(massage_lableframe, text="��   ��:")
pwd = tk.StringVar()
pwd_text = ttk.Entry(massage_lableframe, textvariable=pwd, validatecommand=(nameandpwdentrycheck, '%P'), show='*')
loginbtn = tk.Button(massage_lableframe, text="��¼", command=loginbtn)
user_name.grid(row=1)
uname_text.grid(row=1, column=1, padx=2, pady=3)
password.grid(row=2, padx=2, pady=3)
pwd_text.grid(row=2, column=1, padx=2, pady=3)
loginbtn.grid(row=5, padx=2, pady=3)

change_ip_lableframe = ttk.LabelFrame(controllercenter_lableframe, text="��IP", width=390, height=300)
# radiobutton4 = ttk.Radiobutton(massage_lableframe , text="��", variable=var, value="c", command=radiobuttonDo)
radiobutton6 = ttk.Radiobutton(change_ip_lableframe, text="Ѷ����", variable=var, value="e", command=radiobuttonDo)
radiobutton5 = ttk.Radiobutton(change_ip_lableframe, text="����", variable=var, value="d", command=radiobuttonDo)
high_quality_agent_lableframe = ttk.LabelFrame(change_ip_lableframe, text="���ʴ���", width=390, height=300)
spiderIdlab = ttk.Label(high_quality_agent_lableframe, text="spiderId:")
spiderIdtext = tk.StringVar()
spiderId_text = ttk.Entry(high_quality_agent_lableframe, width=15, textvariable=spiderIdtext, validate='key',
                          validatecommand=(thentrycheck, '%P'))
orderlab = ttk.Label(high_quality_agent_lableframe, text="������:")
ordertext = tk.StringVar()
order_text = ttk.Entry(high_quality_agent_lableframe, width=15, textvariable=ordertext, validate='key',
                       validatecommand=(thentrycheck, '%P'))
use_count_lab = ttk.Label(high_quality_agent_lableframe, text="ʹ�ô���:")
use_count_var = tkinter.StringVar()  # ʹ�ô���
use_count__text = ttk.Combobox(high_quality_agent_lableframe, width=10, textvariable=use_count_var, validate='key',
                               validatecommand=(thentrycheck, '%P'))
use_count__text["values"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
testbutton = tk.Button(high_quality_agent_lableframe, text="����", command=testbtn, width=10)
# radiobutton7 = ttk.Radiobutton(change_ip_lableframe , text="����ip", variable=var, value="f", command=radiobuttonDo)
radiobutton5.grid(row=0, column=1, padx=2, pady=3)
radiobutton6.grid(row=0, column=0, padx=2, pady=3)
# radiobutton7.grid(row=0,column=2,padx=2,pady=3)
spiderIdlab.grid(row=1, column=0, padx=2, pady=3)
spiderId_text.grid(row=1, column=1, padx=2, pady=3)
orderlab.grid(row=2, column=0, padx=2, pady=3)
order_text.grid(row=2, column=1, padx=2, pady=3)
use_count_lab.grid(row=3, column=0, padx=2, pady=3)
use_count__text.grid(row=3, column=1, padx=2, pady=3)
testbutton.grid(row=4, column=0, padx=2, pady=3, sticky=tk.S)

dial_lableframe = ttk.LabelFrame(change_ip_lableframe, text="����", width=390, height=300)
BWaccountlabel = ttk.Label(dial_lableframe, text="����˺�:")
BW_account_var = tk.StringVar()
BWaccount_text = ttk.Entry(dial_lableframe, width=15, textvariable=BW_account_var, validate='key',
                           validatecommand=(thentrycheck, '%P'))
BWpwdlabel = ttk.Label(dial_lableframe, text="�������:")
BWpwd_var = tk.StringVar()
BWpwd_text = ttk.Entry(dial_lableframe, width=15, textvariable=BWpwd_var, validate='key',
                       validatecommand=(thentrycheck, '%P'))
filterIPcheckbtn = ttk.Checkbutton(dial_lableframe, text="������ͬIP")
dialbutton = tk.Button(dial_lableframe, text="���Ų���", command=dailbtn, width=10)
BWaccountlabel.grid(row=0, column=0, padx=2, pady=3)
BWaccount_text.grid(row=0, column=1, padx=2, pady=3)
BWpwdlabel.grid(row=1, column=0, padx=2, pady=3)
BWpwd_text.grid(row=1, column=1, padx=2, pady=3)
filterIPcheckbtn.grid(row=2, column=0, padx=3, pady=3)
dialbutton.grid(row=3, column=0, padx=2, pady=3)

operater_lableframe = ttk.LabelFrame(controllercenter_lableframe, text="������", width=390, height=300)
operater_count_lab = ttk.Label(operater_lableframe, text="������:")
operater_count_var = tk.IntVar()
operater_count_var.set(1)
operater_count_text = ttk.Entry(operater_lableframe, width=10, textvariable=operater_count_var, validate='key',
                                validatecommand=(thentrycheck, '%P'))
thread_count_lab = ttk.Label(operater_lableframe, text="�߳���:")
thread_count_var = tk.IntVar()
thread_count_var.set(1)
thread_count_text = ttk.Entry(operater_lableframe, width=10, textvariable=thread_count_var, validate='key',
                              validatecommand=(thentrycheck, '%P'))
dial_delay_lab = ttk.Label(operater_lableframe, text="�����ӳ�:")
dial_delay_var = tk.IntVar()
dial_delay_var.set(1)
dial_delay_text = ttk.Entry(operater_lableframe, width=10, textvariable=dial_delay_var, validate='key',
                            validatecommand=(thentrycheck, '%P'))
randomPWDcheck = ttk.Checkbutton(operater_lableframe, text="�������")
fixedpwdlab = ttk.Label(operater_lableframe, text="�̶�����:")
fixedpwd_var = tk.IntVar()
fixedpwd_var.set(1)
fixedpwd_text = ttk.Entry(operater_lableframe, width=10, textvariable=fixedpwd_var, validate='key',
                          validatecommand=(thentrycheck, '%P'))
Invite_code = ttk.Label(operater_lableframe, text="������:")
invitation_code_var = tk.StringVar()
invitation_code_text = ttk.Entry(operater_lableframe, width=10, textvariable=invitation_code_var)
runbutton = tk.Button(operater_lableframe, text="����", command=runbtn, width=10)
stopbutton = tk.Button(operater_lableframe, text="ֹͣ", command=stopbtn, width=10)
clearrunninglogbutton = tk.Button(operater_lableframe, text="������м�¼", command=clearRunninglogButton, width=10)
# radiobutton4.grid(row=0,column=3,padx=5,sticky=tk.E)
operater_count_lab.grid(row=0, column=0, padx=2, pady=3)
operater_count_text.grid(row=0, column=1, padx=2, pady=3)
thread_count_lab.grid(row=0, column=2, padx=2, pady=3)
thread_count_text.grid(row=0, column=3, padx=2, pady=3)
dial_delay_lab.grid(row=1, column=2, padx=2, pady=3)
dial_delay_text.grid(row=1, column=3, padx=2, pady=3)
randomPWDcheck.grid(row=2, column=0, padx=2, pady=3)
fixedpwdlab.grid(row=2, column=2, padx=5, pady=3)
fixedpwd_text.grid(row=2, column=3, padx=2, pady=3)
Invite_code.grid(row=4, column=0, padx=2, pady=3)
invitation_code_text.grid(row=4, column=1, padx=2, pady=3)
runbutton.grid(row=6, column=0, padx=5, sticky=tk.S)
stopbutton.grid(row=6, column=1, padx=5, sticky=tk.S)
clearrunninglogbutton.grid(row=6, column=2, padx=5, sticky=tk.S + tk.E)
# ����lableframe�ŵ�tab1��
runninglog_lableframe.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S)
controllercenter_lableframe.grid(row=0, column=1, padx=5, sticky=tk.N)
massage_lableframe.grid(row=0, padx=5, sticky=tk.N + tk.W + tk.E)
change_ip_lableframe.grid(row=1, padx=5)
high_quality_agent_lableframe.grid(row=1, column=0)
dial_lableframe.grid(row=1, column=1)
operater_lableframe.grid(row=2, padx=5, sticky=tk.W)
try:
    with open("account") as fp:
        n, p = fp.read().strip().split(',')
        uname.set(n)
        pwd.set(p)
except:
    pass
# -----------------------------------------------tab2---------------------------------------------------
# ���������б�����

vbar = tkinter.Scrollbar(tab2)
tree = ttk.Treeview(tab2, show="headings", height=18, columns=("a", "b", "c", "d", "e"), yscrollcommand=vbar.set)
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

# =======================������(��������)================
pos = 0


def marquee(widget):
    global source_str
    source_str = "���¹���:��2019��1��1����,VIP��Ա��100Ԫ��100Ԫ"
    testEntry["width"] = 116
    strlen = len(source_str)
    space = "                                    " \
            "                                                                                                                                                                    "
    global pos
    source_str = space + source_str
    # 208
    if pos == len(source_str) + 5:
        pos = 0
    testEntry.delete(0, tk.END)
    testEntry.insert(0, source_str)
    testEntry.delete(0, pos)
    pos += 1
    # print("==============>",len(space))
    if ((len(source_str) - pos) - strlen < 0):
        widget.after(200, marquee, widget)
    else:
        widget.after(100, marquee, widget)


testEntry = tk.Entry(tab1, fg="RED")
marquee(testEntry)
testEntry.grid(row=1, column=0, columnspan=2, sticky=tk.S + tk.E)


# -----------------------���Զ���-------------------------------------
def t():
    w = win()
    w.ttt(tab3)


t()

urlwork.testSrc(ordertext)
root.mainloop()
