# -*- coding: utf-8 -*-
import subprocess
import threading
import tkinter
import tkinter as tk  # 装载tkinter模块,用于Python3
from tkinter import *  # 装载tkinter.ttk模块,用于Python3
import base64
import os
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import time
from configobj import ConfigObj

from About import About
from Help import Help
from Runtest import Runtest
from utils.device import Device
from utils.icon import img


# 主页
class MainFrame:
    def __init__(self):
        self.win = tk.Tk()  # 创建窗口对象
        self.win.title(string='monkeyTools')  # 设置窗口标题
        self.win.resizable(False, False)  # 禁用窗口缩放
        # self.root.geometry('800x600+200+200')
        self.init_position(800, 640)
        self.win.update_idletasks()  #

        # self.root.iconbitmap('icon.ico')
        # 使用icon.py设置图标，兼容pyinstaller打包
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.win.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

        self.initTabMenu()
        # 帮助界面
        help = Help(self.tab3)
        help.initHelp()

        # 关于我们
        about = About(self.tab4)
        about.initAbout()

        self.initConfig()

        # 测试主界面
        self.testMain()

    # 测试主界面
    def testMain(self):

        btnParamsScript = Button(self.tab2, text='根据配置参数生成脚本', command=self.getParamsScript, width=20)
        btnParamsScript.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.commandStr = Text(self.tab2, width=85, height=5, relief="groove", borderwidth=2)
        self.commandStr.grid(row=1, column=1, sticky=E, padx=10, pady=10, ipadx=5, ipady=5)

        # fram = Frame(self.tab2, bg="white")
        # fram.grid(row=2, column=0, sticky=W, padx=10, pady=10, columnspan=2)

        # btnParamsScript = Button(fram, text='日志位置：', width=20)
        # btnParamsScript.grid(row=1, column=0, sticky=W, pady=10)
        #
        # frame_radioButton = Frame(fram)
        # frame_radioButton.grid(row=1, column=1, sticky=W, padx=10, pady=4)
        #
        # #日志保存路径
        # self.logCachePath = IntVar()
        # self.logCachePath.set(2)
        # LANGS = [
        #     ("保存到本地", 1),
        #     ("保存到设备（脱机）", 2)]
        # for lang, num in LANGS:
        #     b = Radiobutton(frame_radioButton, text=lang, variable=self.logCachePath, value=num)
        #     b.pack(side=LEFT, anchor=W)


        fram = Frame(self.tab2, bg="white")
        fram.grid(row=2, column=0, sticky=W, padx=10, pady=0, columnspan=2)

        btnDevice = Button(fram, text='运行脚本', command=self.runOneMonkeyScript, width=15)
        btnDevice.grid(row=1, column=0, sticky=W, padx=0, pady=0)

        btnDevice = Button(fram, text='导出报告', command=self.runTwoMonkeyScript, width=15)
        btnDevice.grid(row=1, column=1, sticky=W, padx=10, pady=0)

        btnDevice = Button(fram, text='打开测试报告目录', command=self.openMonkeyTestReport, width=15)
        btnDevice.grid(row=1, column=2, sticky=W, padx=10, pady=0)

        btnDevice = Button(fram, text='清空日志', command=self.clearLog, width=15)
        btnDevice.grid(row=1, column=3, sticky=W, padx=10, pady=0)

        btnDevice = Button(fram, text='停止测量', command=self.stopRun, width=15)
        btnDevice.grid(row=1, column=4, sticky=W, padx=10, pady=0)

        # 文本域
        self.text = ScrolledText(self.tab2, width=108, height=35, relief="groove", borderwidth=2)
        self.text.configure(state=tkinter.DISABLED)
        self.text.grid(row=3, column=0, sticky=W, padx=10, pady=10, columnspan=2)
        # self.text.place(x=5, y=100, width=470, height=300)
        # 插入数据
        self.text.configure(state=tkinter.NORMAL)
        final_str = ""
        self.text.insert(tk.END, final_str)
        self.text.see(tk.END)

    # 获取脚本
    def getParamsScript(self):
        runtest = Runtest(self)
        runtest.getParamsScript()

    # 运行配置生成的脚本
    def runOneMonkeyScript(self):
        thread = threading.Thread(target=self.runOneMonkeyScriptThread, name='TestThread')
        # thread = threading.Thread(target=test)
        thread.start()

    def runOneMonkeyScriptThread(self):
        runtest = Runtest(self)
        runtest.runOneMonkeyScript()

    # 導出日志
    def runTwoMonkeyScript(self):
        thread = threading.Thread(target=self.runTwoMonkeyScriptThread, name='TestThread')
        # # thread = threading.Thread(target=test)
        thread.start()

    def runTwoMonkeyScriptThread(self):
        # runtest = Runtest(self)
        # runtest.runTwoMonkeyScript()
        logPath = self.logPath.get().strip()
        if len(logPath) <= 0:
            messagebox.showwarning("提示", "日志输出路径不能为空")
            return
        device = self.entryDevice.get();
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return

        entryuninstallAPK = self.getPackageNames()  # entryuninstallAPK.get().strip()
        if len(entryuninstallAPK) <= 0:
            messagebox.showwarning("提示", "包名不能为空")
            return

        self.screen_save_path = logPath + '/screenshots/'
        self.reports_path = logPath + '/reports/'
        self.monkey_path = logPath + '/monkeylogs/'

        # 导出日志
        self.text.insert(tk.END, "\n开始导出monkey日志文件。。。")
        self.text.see(tk.END)
        #logfilename_err = self.monkey_path + device + '_monkey_' + time.strftime("%Y_%m_%d_%H_%M_%S",
        #                                                                                time.localtime()) + '_err.txt'
        #logfilename_verbose = self.monkey_path + device + '_monkey_' + time.strftime("%Y_%m_%d_%H_%M_%S",
        #                                                                                    time.localtime()) + '_verbose.txt'
        # bugreport = "adb pull /sdcard/error.txt   "+logfilename_err
        # ex = subprocess.Popen(bugreport, stdout=subprocess.PIPE, shell=True)
        # ex.wait()
        #
        # bugreport = "adb pull /sdcard/verbose.txt   " + logfilename_verbose
        # ex = subprocess.Popen(bugreport, stdout=subprocess.PIPE, shell=True)
        # out, err = ex.communicate()
        # ex.wait()
        bugreport = "adb pull /sdcard/monkeylog/ " + self.monkey_path
        ex = subprocess.Popen(bugreport, stdout=subprocess.PIPE, shell=True)
        out, err = ex.communicate()
        ex.wait()

        self.text.insert(tk.END, "\n结束导出monkey日志文件。。。"+self.monkey_path )
        self.text.see(tk.END)


        # 导出checkbugreport
        self.text.insert(tk.END, "\n创建bugreport文件")
        self.text.see(tk.END)


        forceStopApp = "adb -s %s shell am force-stop %s" % (device,entryuninstallAPK)
        os.popen(forceStopApp)

        ex = subprocess.Popen("adb -s " + device + "  shell dumpsys batterystats --reset", stdout=subprocess.PIPE,
                              shell=True)
        ex.wait()

        filename = device + '_monkey_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '_bugreport.txt'

        self.chkbugreport_path = logPath + '/chkbugreport/'
        bugreport = "adb -s " + device + " shell  bugreport > " + self.chkbugreport_path + filename
        # os.popen(bugreport)

        self.text.insert(tk.END, "\n开始bugreport文件导出")
        self.text.see(tk.END)

        ex = subprocess.Popen(bugreport, stdout=subprocess.PIPE, shell=True)
        ex.wait()
        self.text.insert(tk.END, "\n导出bugreport文件结束，开始chkbugreport.jar转换文档")
        self.text.see(tk.END)

        chkbugreport = "java -jar %s\\chkbugreport.jar %s" % (".", self.chkbugreport_path + filename)
        os.popen(chkbugreport)

        print(chkbugreport)

        self.text.insert(tk.END, "\nchkbugreport.jar转换结束")
        self.text.see(tk.END)

        pass

    # 清空日志
    def clearLog(self):
        self.text.delete(0.0, tk.END)
        pass

    # 停止运行
    def stopRun(self):
        device = Device()
        issuccess = device.getPid(self.getAdbPath())
        pass

    # 打开测试报告
    def openMonkeyTestReport(self):
        logPath = self.logPath.get().strip()
        if len(logPath) <= 0:
            messagebox.showwarning("提示", "配置界面没有选择日志输出路径")
            return
        os.startfile(logPath)

    # 获取自定义monkey脚本目录
    def get_monkey_path(self):
        result = filedialog.askopenfile()
        if result:
            self.monkeyPath.delete(0, END)
            self.monkeyPath.insert(0, result.name)

    def mainloop(self):
        self.win.mainloop()

    # 初始化窗口大小，居中显示
    def init_position(self, curWidth='', curHight=''):
        '''
              设置窗口大小，并居中显示
              :param root:主窗体实例
              :param curWidth:窗口宽度，非必填，默认200
              :param curHight:窗口高度，非必填，默认200
              :return:无
            '''
        if not curWidth:
            '''获取窗口宽度，默认200'''
            curWidth = self.win.winfo_width()
        if not curHight:
            '''获取窗口高度，默认200'''
            curHight = self.win.winfo_height()
        # print(curWidth, curHight)

        # 获取屏幕宽度和高度
        scn_w, scn_h = self.win.maxsize()
        # print(scn_w, scn_h)

        # 计算中心坐标
        cen_x = (scn_w - curWidth) / 2
        cen_y = (scn_h - curHight) / 2
        # print(cen_x, cen_y)

        # 设置窗口初始大小和位置
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
        self.win.geometry(size_xy)

    def initTabMenu(self):
        self.tabControl = ttk.Notebook(self.win)  # 创建Notebook

        self.tab1 = tk.Frame(self.tabControl, relief=GROOVE, bg='#ffffff')  # 增加新选项卡
        # self.tab1.place(relx=0, rely=0)
        self.tabControl.add(self.tab1, text='配置参数')  # 把新选项卡增加到Notebook

        self.tab2 = tk.Frame(self.tabControl, bg='#ffffff')
        self.tabControl.add(self.tab2, text='测试主界面')

        self.tab3 = tk.Frame(self.tabControl, bg='#ffffff')
        self.tabControl.add(self.tab3, text='使用帮助？')

        self.tab4 = tk.Frame(self.tabControl, bg='#ffffff')
        self.tabControl.add(self.tab4, text='关于软件')

        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.select(self.tab1)  # 选择tab1
        # pass

    # 配置界面初始化
    def initConfig(self):
        canvas = Canvas(self.tab1, relief=SUNKEN,
                        scrollregion=(0, 0, 780, 640))  # , width=800, height=600)  # 创建canvas
        # canvas.place(x=0, y=0)  # 放置canvas的位置
        canvas.pack(side="left", expand=YES, fill=BOTH)
        frame = Frame(canvas, width=780, height=640)  # 把frame放在canvas里
        # frame.place(width=780, height=600)  # frame的长宽，和canvas差不多的
        frame.pack(side="top", fill=BOTH)

        vbar = Scrollbar(self.tab1, orient=VERTICAL)  # 竖直滚动条
        # vbar.place(x=780, width=20, height=600)
        vbar.configure(command=canvas.yview)
        vbar.pack(side="right", fill=Y)
        # hbar = Scrollbar(canvas, orient=HORIZONTAL)  # 水平滚动条
        # hbar.place(x=0, y=165, width=180, height=20)
        # hbar.configure(command=canvas.xview)
        canvas.config(yscrollcommand=vbar.set)  # 设置xscrollcommand=hbar.set,
        canvas.create_window((0, 0), window=frame, anchor="nw")  # create_window

        # 基础操作
        frame_left = tk.LabelFrame(frame, text="基础操作", labelanchor="nw")
        frame_left.place(x=2, y=2, width=778, height=160)

        # adb路径
        labelEvent = Label(frame_left, text='adb路径：')
        labelEvent.grid(row=1, column=0, sticky=E, padx=10, pady=0)
        self.entryAdbPath = Entry(frame_left, width=30)
        self.entryAdbPath.bind("<Button-1>", self.get_adb_path)
        self.entryAdbPath.grid(row=1, column=1, sticky=W, padx=10)

        # 设备ID
        labelEvent = Label(frame_left, text='选择设备：')
        labelEvent.grid(row=1, column=2, sticky=E, padx=10, pady=0)

        # self.entryDevice = Entry(frame_left,width=30)
        # self.entryDevice.grid(row=1, column=3, sticky=W, padx=10)

        self.entryDevice = ttk.Combobox(frame_left)
        self.entryDevice['value'] = ('请选择设备')
        self.entryDevice.current(0)
        self.entryDevice.grid(row=1, column=3, sticky=W, padx=10)

        btnDevice = Button(frame_left, text='获取设备', command=self.getDeivceID)
        btnDevice.grid(row=1, column=4, sticky=W, padx=10, pady=0)

        # 事件执行次数
        labelEvent = Label(frame_left, text='事件执行次数：')
        labelEvent.grid(row=2, column=0, sticky=E, padx=10, pady=0)
        self.eventCount = Entry(frame_left, width=30)
        self.eventCount.grid(row=2, column=1, sticky=W, padx=10)

        # 主activity
        # labelEvent = Label(frame_left, text='默认启动M：')
        # labelEvent.grid(row=2, column=2, sticky=E, padx=10, pady=0)
        # self.mainActivity = Entry(frame_left, width=30)
        # self.mainActivity.grid(row=2, column=3, sticky=W, padx=10)

        # 安装软件
        labelEvent = Label(frame_left, text='apk路径：')
        labelEvent.grid(row=3, column=0, sticky=E, padx=10, pady=0)
        self.entryApkPath = Entry(frame_left, width=30)
        self.entryApkPath.bind("<Button-1>", self.get_apk_path)
        self.entryApkPath.grid(row=3, column=1, sticky=W, padx=10)
        btnInstall = Button(frame_left, text='安装', command=self.installApk)
        btnInstall.grid(row=3, column=2, sticky=W, padx=10, pady=0)

        # 卸载软件
        labelEvent = Label(frame_left, text='apk包名：')
        labelEvent.grid(row=4, column=0, sticky=E, padx=10, pady=0)
        self.entryuninstallAPK = Entry(frame_left, width=30)
        self.entryuninstallAPK.grid(row=4, column=1, sticky=W, padx=10)
        btnUnInstall = Button(frame_left, text='卸载', command=self.uninstallApk)
        btnUnInstall.grid(row=4, column=2, sticky=W, padx=10, pady=0)
        # 启动软件
        btnUnInstall = Button(frame_left, text='启动', command=self.launchApk, anchor="w")
        btnUnInstall.grid(row=4, column=3, sticky=W, padx=10, pady=0)

        # 卸载软件
        labelEvent = Label(frame_left, text='多个应用包名：')
        labelEvent.grid(row=5, column=0, sticky=E, padx=10, pady=0)
        self.entryPageName = Entry(frame_left, width=30)
        self.entryPageName.grid(row=5, column=1, sticky=W, padx=10)
        labelEvent = Label(frame_left, text='(用英文分号隔开，当apk包名为空时有效，此项是多个应用测试)')
        labelEvent.grid(row=5, column=2, sticky=W, padx=10, pady=0, columnspan=3)

        # 路径相关
        frame_log = tk.LabelFrame(frame, text="日志相关", labelanchor="nw")
        frame_log.place(x=2, y=170, width=778, height=80)

        # 设置日志输出
        labelEvent = Label(frame_log, text='日志输出路径：')
        labelEvent.grid(row=1, column=0, sticky=E, padx=10, pady=0)
        self.logPath = Entry(frame_log, width=80)
        self.logPath.bind("<Button-1>", self.get_log_path)
        self.logPath.grid(row=1, column=1, sticky=W, padx=10)

        # 日志级别
        labelEvent = Label(frame_log, text='日志级别：')
        labelEvent.grid(row=2, column=0, sticky=E, padx=10, pady=0)

        frame_radioButton = Frame(frame_log)
        frame_radioButton.grid(row=2, column=1, sticky=W, padx=10, pady=4)

        self.logLevel = IntVar()
        self.logLevel.set(3)
        LANGS = [
            ("精简", 1),
            ("普通", 2),
            ("详细", 3)]
        for lang, num in LANGS:
            b = Radiobutton(frame_radioButton, text=lang, variable=self.logLevel, value=num)
            b.pack(side=LEFT, anchor=W)

        # 事件处理

        frame_event = tk.LabelFrame(frame, text="事件处理(百分比总和不能超过100)", labelanchor="nw", )
        frame_event.place(x=2, y=255, width=778, height=190)

        # seed
        labelEvent = Label(frame_event, text='seed(随机种子值int)：')
        labelEvent.grid(row=1, column=0, sticky=E, padx=10, pady=0)
        self.seed = Entry(frame_event, width=20)
        self.seed.grid(row=1, column=1, sticky=W, padx=10)

        # 不常用事件比例 10
        labelEvent = Label(frame_event, text='anyevent(不常用事件比例percent)：')
        labelEvent.grid(row=1, column=2, sticky=E, padx=10, pady=0)
        self.anyevent = Entry(frame_event, width=20)
        self.anyevent.grid(row=1, column=3, sticky=W, padx=10)

        # 事件间隔时间 默认 300 毫秒
        labelEvent = Label(frame_event, text='throttle(事件间隔时间ms)：')
        labelEvent.grid(row=2, column=0, sticky=E, padx=10, pady=0)
        self.throttle = Entry(frame_event, width=20)
        self.throttle.grid(row=2, column=1, sticky=W, padx=10)

        # 启动activity的事件百分比 100
        labelEvent = Label(frame_event, text='appswitch(启动Activity事件percent)：')
        labelEvent.grid(row=2, column=2, sticky=E, padx=10, pady=0)
        self.appswitch = Entry(frame_event, width=20)
        self.appswitch.grid(row=2, column=3, sticky=W, padx=10)

        # 触摸事件 调整monkey命令触摸事件的百分比。
        labelEvent = Label(frame_event, text='touch(触摸事件percent)：')
        labelEvent.grid(row=3, column=0, sticky=E, padx=10, pady=0)
        self.touch = Entry(frame_event, width=20)
        self.touch.grid(row=3, column=1, sticky=W, padx=10)

        # syskeys 调整系统事件百分比。（这些按键通常由系统保留使用，如Home、Back、Start Call、End Call、音量调节），这个参数的百分比通常比较小。
        labelEvent = Label(frame_event, text='syskeys(系统事件percent)：')
        labelEvent.grid(row=3, column=2, sticky=E, padx=10, pady=0)
        self.syskeys = Entry(frame_event, width=20)
        self.syskeys.grid(row=3, column=3, sticky=W, padx=10)

        # motion 动作手势
        labelEvent = Label(frame_event, text='motion(动作手势事件percent)：')
        labelEvent.grid(row=4, column=0, sticky=E, padx=10, pady=0)
        self.motion = Entry(frame_event, width=20)
        self.motion.grid(row=4, column=1, sticky=W, padx=10)

        # majornav 调整主要导航事件的百分比。（这些导航事件通常会导致UI界面中的动作事件，如5-way键盘的中间键，回退按键、菜单按键），这个参数不常用。
        labelEvent = Label(frame_event, text='majornav (主要导航事件percent)：')
        labelEvent.grid(row=4, column=2, sticky=E, padx=10, pady=0)
        self.majornav = Entry(frame_event, width=20)
        self.majornav.grid(row=4, column=3, sticky=W, padx=10)

        # trackball  调整滚动球事件百分比
        labelEvent = Label(frame_event, text='trackball(滚动球事件percent)：')
        labelEvent.grid(row=5, column=0, sticky=E, padx=10, pady=0)
        self.trackball = Entry(frame_event, width=20)
        self.trackball.grid(row=5, column=1, sticky=W, padx=10)

        # nav  调整基本的导航事件百分比 输入设备上、下、左、右键
        labelEvent = Label(frame_event, text='nav  (基本导航事件percent)：')
        labelEvent.grid(row=5, column=2, sticky=E, padx=10, pady=0)
        self.nav = Entry(frame_event, width=20)
        self.nav.grid(row=5, column=3, sticky=W, padx=10)

        # pct-pinchzoom  缩放事件百分比
        labelEvent = Label(frame_event, text='pinchzoom(缩放事件percent)：')
        labelEvent.grid(row=6, column=0, sticky=E, padx=10, pady=0)
        self.pinchzoom = Entry(frame_event, width=20)
        self.pinchzoom.grid(row=6, column=1, sticky=W, padx=10)

        # rotation 屏幕旋转事件
        labelEvent = Label(frame_event, text='rotation(屏幕旋转事件percent)：')
        labelEvent.grid(row=6, column=2, sticky=E, padx=10, pady=0)
        self.rotation = Entry(frame_event, width=20)
        self.rotation.grid(row=6, column=3, sticky=W, padx=10)

        # trackball  调整滚动球事件百分比
        labelEvent = Label(frame_event, text='flip(键盘翻转事件percent)：')
        labelEvent.grid(row=7, column=0, sticky=E, padx=10, pady=0)
        self.flip = Entry(frame_event, width=20)
        self.flip.grid(row=7, column=1, sticky=W, padx=10)

        # 调试选项
        frame_options = tk.LabelFrame(frame, text="调试选项", labelanchor="nw", )
        frame_options.place(x=2, y=450, width=778, height=110)

        # 如果指定了这个选项，那么monkey会启动待测应用，但是不发送任何消息。最好将其与”-v“、”-p“、和”--throttle“等选项一起使用，并让monkey运行30秒以上，这样可以让我们观测到待测应用在多个包的切换过程

        # -dbg-no-events
        labelEvent = Label(frame_options, text='-dbg-no-events：')
        labelEvent.grid(row=1, column=0, sticky=E, padx=10, pady=0)
        self.dbgNoEventsCheckVar = IntVar(0)
        self.dbgNoEvents = Checkbutton(frame_options, text="", variable=self.dbgNoEventsCheckVar, \
                                       onvalue=1, offvalue=0, height=1, \
                                       width=5, anchor="w")
        self.dbgNoEvents.grid(row=1, column=1, sticky=W, padx=0)

        # –hprof
        labelEvent = Label(frame_options, text='–hprof：')
        labelEvent.grid(row=1, column=2, sticky=E, padx=10, pady=0)
        self.hprofCheckVar = IntVar(0)
        self.hprof = Checkbutton(frame_options, text="", variable=self.hprofCheckVar, \
                                 onvalue=1, offvalue=0, height=1, \
                                 width=5, anchor="w")
        self.hprof.grid(row=1, column=3, sticky=W, padx=0)

        # –ignore-crashes
        labelEvent = Label(frame_options, text='–ignore-crashes：')
        labelEvent.grid(row=1, column=4, sticky=E, padx=10, pady=0)
        self.ignoreCrashesCheckVar = IntVar(0)
        self.ignoreCrashes = Checkbutton(frame_options, text="", variable=self.ignoreCrashesCheckVar, \
                                         onvalue=1, offvalue=0, height=1, \
                                         width=5, anchor="w")
        self.ignoreCrashes.grid(row=1, column=5, sticky=W, padx=0)

        # –ignore-timeouts
        labelEvent = Label(frame_options, text='–ignore-timeouts：')
        labelEvent.grid(row=2, column=0, sticky=E, padx=10, pady=0)
        self.ignoreTimeoutsCheckVar = IntVar(0)
        self.ignoreTimeouts = Checkbutton(frame_options, text="", variable=self.ignoreTimeoutsCheckVar, \
                                          onvalue=1, offvalue=0, height=1, \
                                          width=5, anchor="w")
        self.ignoreTimeouts.grid(row=2, column=1, sticky=W, padx=0)

        # –ignore-security-exception
        labelEvent = Label(frame_options, text='–ignore-security-exception：')
        labelEvent.grid(row=2, column=2, sticky=E, padx=10, pady=0)
        self.ignoreSecurityExceptionCheckVar = IntVar(0)
        self.ignoreSecurity = Checkbutton(frame_options, text="", variable=self.ignoreSecurityExceptionCheckVar, \
                                          onvalue=1, offvalue=0, height=1, \
                                          width=5, anchor="w")
        self.ignoreSecurity.grid(row=2, column=3, sticky=W, padx=0)

        # –kill-process-after-error
        labelEvent = Label(frame_options, text='–kill-process-after-error：')
        labelEvent.grid(row=2, column=4, sticky=E, padx=10, pady=0)
        self.killProcessAfterErrorCheckVar = IntVar(0)
        self.killProcessAfterError = Checkbutton(frame_options, text="", variable=self.killProcessAfterErrorCheckVar, \
                                                 onvalue=1, offvalue=0, height=1, \
                                                 width=5, anchor="w")
        self.killProcessAfterError.grid(row=2, column=5, sticky=W, padx=0)

        # –monitor-native-crashes
        labelEvent = Label(frame_options, text='–monitor-native-crashes：')
        labelEvent.grid(row=3, column=0, sticky=E, padx=10, pady=0)
        self.monitorNativeCrashesCheckVar = IntVar(0)
        self.monitorNativeCrashes = Checkbutton(frame_options, text="", variable=self.monitorNativeCrashesCheckVar, \
                                                onvalue=1, offvalue=0, height=1, \
                                                width=5, anchor="w")
        self.monitorNativeCrashes.grid(row=3, column=1, sticky=W, padx=0)

        # –wait-dbg
        labelEvent = Label(frame_options, text='–wait-dbg：')
        labelEvent.grid(row=3, column=2, sticky=E, padx=10, pady=0)
        self.waitDbgCheckVar = IntVar(0)
        self.waitDbg = Checkbutton(frame_options, text="", variable=self.waitDbgCheckVar, \
                                   onvalue=1, offvalue=0, height=1, \
                                   width=5, anchor="w")
        self.waitDbg.grid(row=3, column=3, sticky=W, padx=0)

        # 保存信息和生成事件
        button = Button(frame, text="重置配置", command=self.resetConfigCallBack, bg="grey")
        button.place(x=135, y=570, width=120, height=30)

        button = Button(frame, text="保存配置", command=self.saveConfigCallBack)
        button.place(x=525, y=570, width=120, height=30)

        # 初始化值
        self.initValue()

    # 初始化值
    def initValue(self):
        # print( sys.path[0]+"===" )
        config = ConfigObj('./config.ini', encoding='UTF-8')
        # if config :
        # print(config['默认']['anyevent'])
        # print(config['自定义']['anyevent'])
        isCustom = config['自定义']['isCustom']
        key = "自定义" if isCustom == '1' else "默认"
        # adb路径
        if config[key]['adb路径']:
            self.entryAdbPath.delete(0, END)
            self.entryAdbPath.insert(0, config[key]['adb路径'])
        else:
            pathStr = os.environ["PATH"]
            if pathStr:
                paths = pathStr.split(";")
                for path in paths:
                    if path.find("platform-tools") >= 0:
                        self.entryAdbPath.delete(0, END)
                        self.entryAdbPath.insert(0, path + "/adb")
        # 设备
        if config[key]['设备名称']:
            self.entryDevice['value'] = (config[key]['设备名称'])
            self.entryDevice.current(0)
        else:
            self.getDeivceID(False)

        self.eventCount.delete(0, END)
        self.eventCount.insert(0, config[key]['事件执行次数'])

        self.entryuninstallAPK.delete(0, END)
        self.entryuninstallAPK.insert(0, config[key]['apk包名'])

        self.entryPageName.delete(0, END)
        self.entryPageName.insert(0, config[key]['多个应用包名'])

        self.logPath.delete(0, END)
        self.logPath.insert(0, config[key]['日志输出路径'])

        self.logLevel.set(config[key]['日志级别'])

        self.seed.delete(0, END)
        self.seed.insert(0, config[key]['seed'])

        self.throttle.delete(0, END)
        self.throttle.insert(0, config[key]['throttle'])

        self.anyevent.delete(0, END)
        self.anyevent.insert(0, config[key]['anyevent'])

        self.appswitch.delete(0, END)
        self.appswitch.insert(0, config[key]['appswitch'])

        self.touch.delete(0, END)
        self.touch.insert(0, config[key]['touch'])

        self.syskeys.delete(0, END)
        self.syskeys.insert(0, config[key]['syskeys'])

        self.motion.delete(0, END)
        self.motion.insert(0, config[key]['motion'])

        self.majornav.delete(0, END)
        self.majornav.insert(0, config[key]['majornav'])

        self.trackball.delete(0, END)
        self.trackball.insert(0, config[key]['trackball'])

        self.nav.delete(0, END)
        self.nav.insert(0, config[key]['nav'])

        self.pinchzoom.delete(0, END)
        self.pinchzoom.insert(0, config[key]['pinchzoom'])

        self.rotation.delete(0, END)
        self.rotation.insert(0, config[key]['rotation'])

        self.flip.delete(0, END)
        self.flip.insert(0, config[key]['flip'])
        # 调试选项
        self.dbgNoEventsCheckVar.set(config[key]['events'])
        self.hprofCheckVar.set(config[key]['hprof'])
        self.ignoreCrashesCheckVar.set(config[key]['crashes'])
        self.ignoreTimeoutsCheckVar.set(config[key]['timeouts'])
        self.ignoreSecurityExceptionCheckVar.set(config[key]['exception'])
        self.killProcessAfterErrorCheckVar.set(config[key]['processAfterError'])
        self.monitorNativeCrashesCheckVar.set(config[key]['monitorNativeCrashes'])
        self.waitDbgCheckVar.set(config[key]['waitDbg'])

    # 保存配置
    def saveConfigCallBack(self):
        config = ConfigObj('./config.ini', encoding='UTF-8')
        config['自定义']['isCustom'] = 1
        config['自定义']['adb路径'] = self.entryAdbPath.get()
        device = self.entryDevice.get();
        if device.find("选择设备") < 0:
            config['自定义']['设备名称'] = device
        config['自定义']['事件执行次数'] = self.eventCount.get()
        config['自定义']['apk包名'] = self.entryuninstallAPK.get()
        config['自定义']['多个应用包名'] = self.entryPageName.get()
        config['自定义']['日志输出路径'] = self.logPath.get()
        config['自定义']['日志级别'] = self.logLevel.get()
        config['自定义']['seed'] = self.seed.get()
        config['自定义']['throttle'] = self.throttle.get()
        config['自定义']['touch'] = self.touch.get()
        config['自定义']['motion'] = self.motion.get()
        config['自定义']['pinchzoom'] = self.pinchzoom.get()
        config['自定义']['trackball'] = self.trackball.get()
        config['自定义']['rotation'] = self.rotation.get()
        config['自定义']['nav'] = self.nav.get()
        config['自定义']['majornav'] = self.majornav.get()
        config['自定义']['syskeys'] = self.syskeys.get()
        config['自定义']['appswitch'] = self.appswitch.get()
        config['自定义']['flip'] = self.flip.get()
        config['自定义']['anyevent'] = self.anyevent.get()
        config['自定义']['events'] = self.dbgNoEventsCheckVar.get()
        config['自定义']['hprof'] = self.hprofCheckVar.get()
        config['自定义']['crashes'] = self.ignoreCrashesCheckVar.get()
        config['自定义']['timeouts'] = self.ignoreTimeoutsCheckVar.get()
        config['自定义']['exception'] = self.ignoreSecurityExceptionCheckVar.get()
        config['自定义']['processAfterError'] = self.killProcessAfterErrorCheckVar.get()
        config['自定义']['monitorNativeCrashes'] = self.monitorNativeCrashesCheckVar.get()
        config['自定义']['waitDbg'] = self.waitDbgCheckVar.get()
        config.write()
        messagebox.showwarning("提示", "保存成功")

    # 重置配置
    def resetConfigCallBack(self):
        config = ConfigObj('./config.ini', encoding='UTF-8')
        config['自定义']['isCustom'] = 0
        config.write()
        self.initValue()
        messagebox.showwarning("提示", "重置成功")

    # 日志输出路径设置
    def get_log_path(self, event):
        dirname = tk.filedialog.askdirectory()  # 返回文件名
        if dirname:
            self.logPath.delete(0, END)
            self.logPath.insert(0, dirname)

    # 启动apk
    def launchApk(self):
        apkPath = self.entryuninstallAPK.get()
        if apkPath == "":
            messagebox.showwarning("提示", "请输入包名")
            return

        device = self.entryDevice.get();
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return
        # mainActivity = self.mainActivity.get()
        # if mainActivity == '':
        #     messagebox.showwarning("提示", "请输入默认启动的Activity")
        #     return
        cmd = self.getAdbPath() + ' -s ' + device + ' shell  monkey -p ' + apkPath + ' -c android.intent.category.LAUNCHER 1'
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        print('rt:' + rt)
        if rt.find("No activities") >= 0:
            messagebox.showwarning("提示", "启动apk失败")
            return
        messagebox.showwarning("提示", "启动apk成功")

    # 卸载apk
    def uninstallApk(self):
        apkPath = self.entryuninstallAPK.get()
        if apkPath == "":
            messagebox.showwarning("提示", "请输入包名")
            return

        device = self.entryDevice.get();
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return

        cmd = self.getAdbPath() + ' -s ' + device + ' uninstall ' + apkPath
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        print('rt:' + rt)
        if rt.find("Success") >= 0:
            messagebox.showwarning("提示", "卸载apk成功")
            return
        messagebox.showwarning("提示", "卸载apk失败")

    # 获取apk 路径
    def get_apk_path(self, event):
        result = filedialog.askopenfile()
        if result:
            self.entryApkPath.delete(0, END)
            self.entryApkPath.insert(0, result.name)

    # 安装apk
    def installApk(self):
        apkPath = self.entryApkPath.get()
        if apkPath == "":
            messagebox.showwarning("提示", "请先选择apk路径")
            return
        device = self.entryDevice.get();
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return
        cmd = self.getAdbPath() + ' -s ' + device + ' install ' + apkPath
        # print('命令:' + cmd)
        rt = os.popen(cmd).read()
        # print('rt:'+rt)
        if rt.find("Success") >= 0:
            messagebox.showwarning("提示", "安装apk成功")
            return
        messagebox.showwarning("提示", "安装apk失败")

    # 获取adb路径
    def get_adb_path(self, event):
        result = filedialog.askopenfile()
        if result:
            self.entryAdbPath.delete(0, END)
            self.entryAdbPath.insert(0, result.name)

    # 获取设备列表
    def getDeivceID(self, isHint=True):

        device = Device()
        devices = device.get_deviceid_list(self.getAdbPath())

        if devices == False:
            if isHint:
                messagebox.showwarning("提示", "缺少adb环境，请先配置android SDK")
            return

        if len(devices) <= 0:
            if isHint:
                messagebox.showwarning("提示", "没有获取到设备列表，请先插入设备")

        if len(devices) <= 0:
            devices = ('请选择设备')

        self.entryDevice['value'] = devices
        self.entryDevice.current(0)

    # 获取adb路径 自定义或者直接使用系统path 路径
    def getAdbPath(self):
        adbPath = self.entryAdbPath.get()
        if adbPath == '':
            return "adb"
        return adbPath

    # 获取等级字符串
    def getLogLevelStr(self):
        logLevel = self.logLevel.get()
        i = 0
        vStr = ' '
        while (i < logLevel):
            vStr += ' -v '
            i = i + 1
        return vStr

    # 获取包名
    def getPackageNames(self):
        # 单个应用
        entryuninstallAPK = self.entryuninstallAPK.get().strip()

        if len(entryuninstallAPK) > 0:
            return ' -p ' + entryuninstallAPK + ' '

        # 多个包名
        entryPageName = self.entryPageName.get().strip()
        if len(entryPageName) <= 0:
            return ""

        packagesStr = ""

        packages = entryPageName.split(";")
        for package in packages:
            packagesStr = " -p " + package + " "
        return packagesStr


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
