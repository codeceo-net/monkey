'''设备操作类'''
import os
import time

'''teky'''
class DeviceCtrl():

    def __init__(self, deviceid):
        self.deviceid = deviceid
        self.width = 0
        self.height = 0
    def getversion(self):
        '''获取版本号'''
        cmd = 'adb -s ' + self.deviceid + ' shell getprop ro.build.version.release'
        #adb shell getprop ro.build.version.release
        print('命令:' + cmd)
        return os.popen(cmd).read().strip()
    def wakeup(self):
        '''点亮并解锁'''
        #自动化点亮并滑动解锁
        self.getdisplaysize()
        self.trywakeup()
        self.set_screen_off_timeout(10)
        time.sleep(1)
        self.unlock_by_swipe()
        self.presshome()

    def getdisplaysize(self):
        '''得到屏幕分辨率'''
        cmd = 'adb -s ' + self.deviceid + ' shell wm size'
        print('命令:' + cmd)
        rt = os.popen(cmd).read()

        if rt.find('size:')>0:
            rt = rt.split(': ')
            rt = rt[1].split('x')
            self.width = int(rt[0])
            self.height = int(rt[1])

    def trywakeup(self):
        '''执行唤醒返回TRUE，原来是点亮的返回FAlSE'''
        cmd = 'adb -s ' + self.deviceid + ' shell dumpsys window policy | grep \"mScreenOnFully\" '
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if rt.find('mScreenOnFully=false') >= 0:  # 锁屏 按下power点亮
            self.presspower()  # KEYCODE_POWER
            print('点亮屏幕')
            return True
        else:
            return False

    def set_screen_off_timeout(self, minute):
        '''设置锁屏时间'''
        cmd = 'adb -s ' + self.deviceid + ' shell settings put system screen_off_timeout ' + str(minute*60000)
        os.popen(cmd).read()
        print('设置锁屏时间' + str(minute) + '分钟')

    def unlock_by_swipe(self):
        '''常规向上滑动解锁'''
        x1 = x2 = str(self.width/2)
        y1 = str(self.height/2 + self.height/3)
        y2 = str(self.height/2 - self.height/3)
        cmd = 'adb -s ' + self.deviceid + ' shell input swipe ' + x1 + ' '+ y1 + ' ' + x2 + ' ' + y2 + ' 200'
        print('命令:' + cmd)
        os.popen(cmd)

    def presshome(self):
        self.sendkeycode(KeyCodes.KEYCODE_HOME)
        time.sleep(1)
    def sendkeycode(self, keycode):
        '''模拟按键'''
        cmd = 'adb -s ' + self.deviceid + ' shell input keyevent ' + str(keycode)
        os.popen(cmd)
        #print('命令:' + cmd)

    def screenshot(self, filepath):
        '''获取uiautomator dump'''
        try:
            cmd = 'adb -s ' + self.deviceid + ' shell screencap -p  /storage/sdcard0/screen.png'
            # print('命令:' + cmd)
            os.popen(cmd)
            time.sleep(2)
            self.adbpull('/storage/sdcard0/screen.png', filepath)  # 卡死?
            time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            return
    def adbpull(self, srcpath, despath):
        '''adb push'''
        cmd = 'adb -s ' + self.deviceid + ' pull ' + srcpath + ' ' + despath
        #print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if not rt.find('pulled')>=0:
            print(rt)

#定义keycode信息
class KeyCodes():
    KEYCODE_MENU = 1
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_POWER = 26