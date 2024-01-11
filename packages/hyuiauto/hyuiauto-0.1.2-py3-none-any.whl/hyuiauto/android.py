
from ppadb.client import Client
from ppadb.device import Device as PPDevice
import os,time,platform
from pprint import pprint 
import pathlib
from functools import cached_property

TOOLS_DIR =  pathlib.Path(__file__).parent/'tools'
ADB_EXE = (TOOLS_DIR/'android'/'adb.exe').resolve() if platform.system() == 'Windows' else 'adb'
IME_APK = (TOOLS_DIR/'android'/'ADBKeyboard.apk').resolve()

class DeviceCommon:

    # def __init__(self) -> None:
    #     self.ocr = None


    @cached_property
    def ocr(self):
        # Getting called means no custom OCR, use default OCR
        from .ocr import CFG
        return CFG.Default_OCR()


    def screenToText(self, range=None):
        return self.ocr.imgToText(self.screenCap(), cropRange=range)

    def screenToTexts(self, range=None, debug=False):
        items = self.ocr.imgToTexts(self.screenCap(), cropRange=range)

        newItems = []

        if range:
            baseX, baseY =  range[0], range[1]
        else:
            baseX, baseY =  0,0
        
        for item in items:
            
            coord, ele = item
            # name, confidence = ele
            # coord[0]，  coord[2] 分别是左上，右下 的坐标
            x1,y1, x2,y2 = *coord[0],  *coord[2]
            newItems.append([(baseX+x1,baseY+y1, baseX+x2,baseY+y2),ele])
        
        if debug:            
            pprint(newItems, indent=2)

        return newItems
    
        # return result as the following format
        '''
        [ 
            [ 
                (747.0, 796.0, 1020.0, 841.0),  
                ('表格', 0.9990993738174438)
            ],
            [ 
                (747.0, 796.0, 1020.0, 841.0),
                ('取消', 0.9738937616348267)
            ]
        ]'''


    def textPosOnScreen(self, text:str, exact=True, range=None, timeout=10, ocrRet=None):

        startTime = time.time()
        while True:            
            if ocrRet is None:
                items = self.screenToTexts(range) 
            else:
                items = ocrRet

            for item in items:
                # print(item)
                coord, ele = item
                name, confidence = ele
                # print(name,coord)
                
                compareRet = text == name.strip() if exact else text in name.strip()
                if compareRet:
                    return coord
            else:
                curTime = time.time()
                if ocrRet or (curTime-startTime) > timeout:
                    raise RuntimeError(f'`{text}` not on screen')
                
                time.sleep(1)


    def textPosOnScreen_accurate(self, text:str, exact=True, range=None, timeout=10, ocrRet=None):
        
        startTime = time.time()
        while True:            
            if ocrRet is None:
                items = self.screenToTexts() 
            else:
                items = ocrRet

            for item in items:
                # print(item)
                coord, ele = item
                name, confidence = ele
                # print(name,coord)
                
                compareRet = text == name.strip() if exact else text in name.strip()
                if compareRet:
                    if range: # has range limit
                        # coord[0]，  coord[2] 分别是左上，右下 的坐标
                        if  range[0] > coord[0][0]  or range[1] > coord[0][1] or \
                            range[2] < coord[2][0]  or range[3] < coord[2][1]: 
                            continue
                    # x = (coord[0][0] + coord[1][0])/2
                    # y = (coord[0][1] + coord[2][1])/2
                    return (*coord[0],  *coord[2])
            else:
                curTime = time.time()
                if ocrRet or (curTime-startTime) > timeout:
                    raise RuntimeError(f'`{text}` not on screen')
                
                time.sleep(1)


    def tapTextOnScreen(self, text:str, exact=True, range=None, timeout=10, holdTime=0,ocrRet=None):
        x1,y1, x2,y2 = self.textPosOnScreen(text, exact, range, timeout, ocrRet)
        
        x = (x1 + x2)/2
        y = (y1 + y2)/2

        if holdTime == 0:
            self.tap(x,y)
        else:
            self.longPress(x,y,holdTime) 

        return x,y

    
    def waitForTextOnScreen(self, text:str, exact=True, range=None, timeout=10):
        return self.textPosOnScreen(text, exact=exact, range=range, timeout=timeout)
        
        # startTime = time.time()
        # while True:
        #     ret = self.screenToTexts(range=range) # crop image for better performance  
        #     pos = self.textPosOnScreen(text, ocrRet=ret)
        #     if pos:
        #         return
        #     time.sleep(0.5)
        #     curTime = time.time()
        #     if (curTime-startTime) > timeout:
        #         raise RuntimeError(f'`{text}` does not appear on screen in {timeout} seconds')
            
    
    def waitForTextNotOnScreen(self, text:str, exact=True, range=None, timeout=10):
        startTime = time.time()

        while True:
            try:
                pos = self.textPosOnScreen(text, exact=exact, range=range, timeout=0)
            except Exception as e:
                if 'not on screen' in e:
                    return
                raise

            time.sleep(0.5)
            curTime = time.time()
            if (curTime-startTime) > timeout:
                raise RuntimeError(f'`{text}` remain on screen for {timeout} seconds')
            
            
    

class AndroidDevice(PPDevice, DeviceCommon):
    def __init__(self, device):
        # super().__init__(device.client, device.serial)        
        PPDevice.__init__(self, device.client, device.serial)
        DeviceCommon.__init__(self)

        self.tap = self.input_tap
        self.swipe = self.input_swipe
        self.keyEvent = self.input_keyevent        

    def goBack(self):
        self.shell('input keyevent KEYCODE_BACK')

    def longPress(self, x, y, holdTime):
        self.swipe(x,y,x,y,holdTime) # long press

    def screenCap(self):
        scrPng = bytes(super().screencap())
        #with open('tmp.png','wb') as f:
        #    f.write(scrPng)
        return scrPng
        
    def openApp(self, packageName:str):
        self.shell(f'monkey -p {packageName} 1')
        # self.shell(f'am start -n {packageName}')

    def installInputApk(self):
        if self.shell('pm list packages com.android.adbkeyboard'):
                print('adbkeyboard IME already installed')
                # pass

        else:
            print('adbkeyboard IME not installed, install', IME_APK)
            self.install(IME_APK)
            time.sleep(1.5)

        self.shell('ime enable  com.android.adbkeyboard/.AdbIME')
        self.shell('ime set com.android.adbkeyboard/.AdbIME')

        time.sleep(1)
        
    def inputString(self, inStr, endWithOK=False):
        cmd = f'am broadcast -a ADB_INPUT_TEXT --es msg "{inStr}"'
        self.shell(cmd)

        if endWithOK:
            self.shell('am broadcast -a ADB_EDITOR_CODE --ei code 2')
            self.shell('am broadcast -a ADB_EDITOR_CODE --ei code 6')
            # https://developer.android.com/reference/android/view/KeyEvent
            # self.input_keyevent('input keyevent 66')




class AndroidConnector(Client):
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port

        try:
            conn = self.create_connection(timeout=1)
        except: 
            # print('adb server not running, try to lauch it...',end='')
            os.system(f'"{ADB_EXE}" -a start-server')
            print('ok')
            
            try:
                conn = self.create_connection(timeout=1)
            except: 
                print('adb server start failed!')
                raise RuntimeError("ERROR: adb server start failed!")
            
        conn.close()
    
    def devices(self) -> list[AndroidDevice]:
        retList = []
        for device in super().devices():            
            output = device.shell(
                "getprop | grep -E 'ro.product.manufacturer|ro.product.model|ro.product.name|ro.serialno'")
            if 'ro.product.model' not in output:
                continue
            
            devInfo = {}
            for line in output.splitlines():  
                # print(line)          
                for name, item in {
                    'manufacturer':'[ro.product.manufacturer]',
                    'model':'[ro.product.model]',
                    'name':'[ro.product.name]',
                    'sn' :'[ro.serialno]'
                }.items():
                    if line.startswith(item):
                        devInfo[name] = line.split(':')[-1].replace('[','').replace(']','').strip()
            
            aDevice = AndroidDevice(device) 
            aDevice.__devinfo__ = devInfo
            retList.append(aDevice)
        return retList
    
    def firstDevice(self, installInputApk=True) -> AndroidDevice:
        devices = self.devices()
        if not devices :
            return None
    
        if installInputApk:
            devices[0].installInputApk()
        
        return devices[0]

    def device(self, manufacturer=None, model=None, sn=None, installInputApk=True ) -> AndroidDevice:
        devices = self.devices()
        if not devices :
            return None
    
        for d in devices:
            dinfo = d.__devinfo__

            if manufacturer is not None:
                if dinfo['manufacturer'] != manufacturer:
                    continue

            if model is not None:
                if dinfo['model'] != model:
                    continue

            if sn is not None:
                if dinfo['sn'] != sn:
                    continue

            if installInputApk:
                d.installInputApk()
            return d
        
        return None

def showCurrentAppPackageName(debug=False, deviceSn=None):
    
    ac = AndroidConnector()
    if deviceSn is None:
        device = ac.firstDevice(installInputApk=False)
        if device is None:
            print('no device attached!')
            return 'no device attached!'
    else:
        for dev in ac.devices():
            if dev.__devinfo__['sn'] == deviceSn:
                device = dev
                break
        else:
            return 'error'
        
    # old version android does not have 'head' command built-in.
    # output = device.shell(f"dumpsys activity recents | grep 'intent={{' | head -n{lines}")
    output = device.shell(f"dumpsys activity recents | grep 'intent={{'")    
    import re
    pat = 'cmp=(?P<pack>.+)/(?P<act>.+)}'
    for line in output.splitlines():
        if 'intent={' in line:
            if debug:
                print(line)
            for one in re.finditer(pat, line):
                pack = one.group('pack')
                act  = one.group('act')
                resultStr = pack # f"{pack}/{act}"
                print('\n' + resultStr)
                return resultStr

            # if lines > 1:
            #     print('\n-----------------\n')

    return 'error'


def getDeviceCurrentScreenPng(deviceSn=None):
    ac = AndroidConnector()
    device = ac.device(sn=deviceSn)

    if device is None:
        if deviceSn is None:
            err = 'no device attached!'   
        else:
            err = f'device:{deviceSn} not found!'
        print(err)
        return err

    return device.screenCap()
    

def listDevices():    
    ac = AndroidConnector()
    devices = ac.devices()
    return [d.__devinfo__ for d in devices]
