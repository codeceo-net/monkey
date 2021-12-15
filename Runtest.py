import os
from tkinter import messagebox, END, INSERT

import tkinter as tk  # 装载tkinter模块,用于Python3

from test.Task import Task


class Runtest:
    def __init__(self,main= None):
        self.main = main
    #运行文件脚本
    def runTwoMonkeyScript(self):
        monkeyPath = self.main.monkeyPath.get().strip()
        if len( monkeyPath ) <= 0 :
            messagebox.showwarning("提示", "请选择自定义脚本路径")
            return
        device = self.main.entryDevice.get().strip()
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return

        adbPath = self.main.entryAdbPath.get().strip()
        if len( adbPath ) <=0 :
            messagebox.showwarning("提示", "请选择adb路径")
            return

        runcount = self.main.runcount.get().strip()
        if len(runcount) <= 0:
            messagebox.showwarning("提示", "至少执行一次")
            return

        commandStr = self.main.getAdbPath() + ' -s ' + device + ' shell monkey ' + self.main.getLogLevelStr() + '  -f ' + monkeyPath +' '+ runcount
        print('命令:' + commandStr)

        device = self.main.entryDevice.get().strip()

        # testPerson = self.main.testPerson.get().strip()
        # if len(testPerson) <= 0:
        #     messagebox.showwarning("提示", "请填写测试人员")
        #     return
        # modulename = self.main.modulename.get().strip()
        # if len(modulename) <= 0:
        #     messagebox.showwarning("提示", "请填写项目名称")
        #     return
        # apkversion = self.main.apkversion.get().strip()
        # if len(apkversion) <= 0:
        #     messagebox.showwarning("提示", "请填写版本号")
        #     return

        logPath = self.main.logPath.get().strip()
        self.screen_save_path = logPath + '/screenshots/'
        self.reports_path = logPath + '/reports/'
        self.monkey_path = logPath + '/monkeylogs/'

        result = Task(device, "1.0.0", "健康一体机", "test01", self.screen_save_path, self.reports_path,
                      self.monkey_path, commandStr, self.main.text).start()
        self.main.text.insert(tk.END, "\n结果:执行完成")
        self.main.text.see(tk.END)

    #运行命令配置
    def runOneMonkeyScript(self):
        commandStr = self.main.commandStr.get(1.0, END).strip()
        if len( commandStr )<= 0:
            messagebox.showwarning("提示", "还没脚本内容，请先根据配置参数生成脚本")
            return
        device = self.main.entryDevice.get().strip()

        # testPerson = self.main.testPerson.get().strip()
        # if len( testPerson ) <= 0:
        #     messagebox.showwarning("提示", "请填写测试人员")
        #     return
        # modulename = self.main.modulename.get().strip()
        # if len( modulename ) <= 0 :
        #     messagebox.showwarning("提示", "请填写项目名称")
        #     return
        # apkversion = self.main.apkversion.get().strip()
        # if len(apkversion) <= 0:
        #     messagebox.showwarning("提示", "请填写版本号")
        #     return

        logPath = self.main.logPath.get().strip()
        self.screen_save_path = logPath + '/screenshots/'
        self.reports_path = logPath + '/reports/'
        self.monkey_path = logPath + '/monkeylogs/'
        result = Task(device, "1.0", "健康一体机" ,"test01" ,self.screen_save_path,self.reports_path ,self.monkey_path , commandStr,self.main.text).start()
        self.main.text.insert(tk.END, "\n结果:执行完成")
        self.main.text.see(tk.END)

    #生成脚本
    def getParamsScript(self):
        device = self.main.entryDevice.get().strip()
        if device.find("选择设备") > 0:
            messagebox.showwarning("提示", "请先选择设备")
            return
        adbPath = self.main.entryAdbPath.get().strip()
        if len(adbPath) <= 0:
            messagebox.showwarning("提示", "请选择adb路径")
            return

        eventCount = self.main.eventCount.get().strip()
        if len(eventCount) <= 0 or int(eventCount) <= 0:
            messagebox.showwarning("提示", "时间执行次数不能为0")
            return

        entryuninstallAPK = self.main.getPackageNames()#entryuninstallAPK.get().strip()
        if len(entryuninstallAPK) <= 0 :
            messagebox.showwarning("提示", "包名不能为空")
            return

        logPath = self.main.logPath.get().strip()
        if len(logPath) <= 0:
            messagebox.showwarning("提示", "日志输出路径不能为空")
            return

        #创建日志目录
        self.screen_save_path = logPath + '/screenshots/'
        self.reports_path = logPath + '/reports/'
        self.monkey_path = logPath + '/monkeylogs/'
        self.chkbugreport_path = logPath + '/chkbugreport/'
        if not os.path.exists(self.screen_save_path):
            os.makedirs(self.screen_save_path)
        if not os.path.exists(self.reports_path):
            os.makedirs(self.reports_path)
        if not os.path.exists(self.monkey_path):
            os.makedirs(self.monkey_path)
        if not os.path.exists(self.chkbugreport_path):
            os.makedirs(self.chkbugreport_path)

        self.LogLevelStr = self.main.getLogLevelStr()

        seed = self.main.seed.get().strip()
        if len(seed) <= 0:
            messagebox.showwarning("提示", "seed随机种子不能为空")
            return

        throttle = self.main.throttle.get().strip()
        if len(throttle) <= 0:
            messagebox.showwarning("提示", "事件间隔时间")
            return

        eventsStr = ""

        anyevent = self.main.anyevent.get().strip()
        anyevent = 13 if len( anyevent ) <= 0 or int( anyevent )<=0 else anyevent
        if int( anyevent )>0 :
            eventsStr += " --pct-anyevent " + anyevent


        appswitch = self.main.appswitch.get().strip()
        appswitch = 8 if len(appswitch) <= 0 or int(appswitch)<=0 else appswitch
        if int( appswitch ) >0:
            eventsStr += " --pct-appswitch " + appswitch

        touch = self.main.touch.get().strip()
        touch = 25 if len(touch) <= 0 or int(touch)<=0 else touch
        if int( touch ) >0:
            eventsStr += " --pct-touch " + touch

        syskeys = self.main.syskeys.get().strip()
        syskeys = 2 if len(syskeys) <= 0 or int(syskeys)<=0 else syskeys
        if int( syskeys) >0 :
            eventsStr += " --pct-syskeys " + syskeys

        motion = self.main.motion.get().strip()
        motion = 10 if len(motion) <= 0 or int(motion)<=0 else motion
        if int( motion  )>0:
            eventsStr += " --pct-motion " + motion

        majornav = self.main.majornav.get().strip()
        majornav = 10 if len(majornav) <= 0 or int(majornav)<=0 else majornav
        if int( majornav  )>0:
            eventsStr += " --pct-majornav " + majornav

        trackball = self.main.trackball.get().strip()
        trackball = 5 if len(trackball) <= 0 or int(trackball)<=0 else trackball
        if int( trackball  )>0:
            eventsStr += " --pct-trackball " + trackball

        nav = self.main.nav.get().strip()
        nav = 25 if len(nav) <= 0 or int(nav)<=0 else nav
        if int( nav) >0 :
            eventsStr += " --pct-nav " + nav

        pinchzoom = self.main.pinchzoom.get().strip()
        pinchzoom = 2 if len(pinchzoom) <= 0 or int(pinchzoom)<=0 else pinchzoom
        if int( pinchzoom ) >0:
            eventsStr += " --pct-pinchzoom " + pinchzoom

        rotation = self.main.rotation.get().strip()
        rotation = 0 if len(rotation) <= 0 or int(rotation)<=0 else rotation
        if int( rotation  )>0:
            eventsStr += " --pct-rotation " + rotation

        flip = self.main.flip.get().strip()
        flip = 0 if len(flip) <= 0 or int(flip)<=0 else flip
        if int( flip )>0 :
            eventsStr += " --pct-flip " + flip

        print( "eventsStr="+eventsStr )

        debugOptions = ""

        dbgNoEventsCheckVar = int(self.main.dbgNoEventsCheckVar.get())
        if dbgNoEventsCheckVar > 0 :
            debugOptions += " --dbg-no-events "

        hprofCheckVar = int(self.main.hprofCheckVar.get())
        if hprofCheckVar > 0:
            debugOptions += " --hprof "

        ignoreCrashesCheckVar = int(self.main.ignoreCrashesCheckVar.get())
        if ignoreCrashesCheckVar > 0:
            debugOptions += " --ignore-crashes "

        ignoreTimeoutsCheckVar = int(self.main.ignoreTimeoutsCheckVar.get())
        if ignoreTimeoutsCheckVar > 0:
            debugOptions += " --ignore-timeouts "

        ignoreSecurityExceptionCheckVar = int(self.main.ignoreSecurityExceptionCheckVar.get())
        if ignoreSecurityExceptionCheckVar > 0:
            debugOptions += " --ignore-security-exceptions "

        killProcessAfterErrorCheckVar = int(self.main.killProcessAfterErrorCheckVar.get())
        if killProcessAfterErrorCheckVar > 0:
            debugOptions += " --kill-process-after-error "

        monitorNativeCrashesCheckVar = int(self.main.monitorNativeCrashesCheckVar.get())
        if monitorNativeCrashesCheckVar > 0:
            debugOptions += " --monitor-native-crashes "

        waitDbgCheckVar = int(self.main.waitDbgCheckVar.get())
        if waitDbgCheckVar > 0:
            debugOptions += " --wait-dbg "

        print( debugOptions )

        command = adbPath + " -s " + device + " shell monkey -s " + seed + entryuninstallAPK + ' --throttle ' + throttle +' '+ eventsStr\
                  + " "+ debugOptions +  self.LogLevelStr + eventCount

        self.main.commandStr.delete(1.0, END)
        self.main.commandStr.insert(INSERT, command )




