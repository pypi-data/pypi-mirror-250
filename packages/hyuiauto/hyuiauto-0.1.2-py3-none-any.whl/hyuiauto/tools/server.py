from bottle import get, static_file, run, request, response
from json import dumps
import subprocess, os, platform, threading,sys,traceback,time
from ..android import *


HTTP_PORT = 18477

curFileDir = os.path.dirname(os.path.abspath(__file__))
staticRoot = os.path.join(curFileDir,'z_dist')

latest_screen = b'' # lastest screenshot png data
ocr = None 

# Static Routes
@get('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=staticRoot)


@get('/api/android/get-devices')
def getDevices():
    devices = listDevices()
    response.content_type = 'application/json'
    return dumps({
        'devices' : devices
    })

@get('/api/android/device/get-current-package')
def getDeviceCurApp():
    sn = request.GET.get('devicesn', '').strip()
    
    retStr = showCurrentAppPackageName(deviceSn=sn,debug=True)

    response.content_type = 'application/json'
    return dumps({'ret':retStr})


@get('/api/android/device/get-current-screen')
def getCurrentScreen():
    global latest_screen
    sn = request.GET.get('devicesn', '').strip()
    
    ret = getDeviceCurrentScreenPng(sn)
    if type(ret) == str:
        response.status = 400
        response.content_type = 'application/json'
        return dumps({'error': ret})

    response.content_type = 'image/png'
    latest_screen = ret # save screenshot as the latest screen
    return ret



@get('/api/do-ocr-of-lastest-screen')
def ocrOfLastestScreen():
    global latest_screen, ocr
    from hyuiauto.ocr import CFG

    response.content_type = 'application/json'

    png_data = latest_screen

    time1 = time.time()

    if ocr is None:
        ocr =  CFG.Default_OCR()


    engine = request.GET.get('ocr_engine', '').strip()
    if engine:
        ocr.setOcrEngine(engine)

    # if crop
    left_top_right_bottom = request.GET.get('left_top_right_bottom', '')
    if left_top_right_bottom:
        range = eval(left_top_right_bottom)
        items = ocr.imgToTexts(png_data, cropRange=range)
        baseX, baseY =  range[0], range[1]
    else:
        items = ocr.imgToTexts(png_data)
        baseX, baseY =  0,0
    

    ret = ''
    for item in items:
        # print(item)
        coord, ele = item
        name, confidence = ele
        # coord[0]，  coord[2] 分别是左上，右下 的坐标
        x1,y1, x2,y2 = *coord[0],  *coord[2]
    
        ret +=f'{(baseX+x1,baseY+y1, baseX+x2,baseY+y2)}  {name}'+'\n'
                


    time3 = time.time()
    duration = time3-time1
    print('all takes', duration)
    return dumps({'ret':ret,'duration':"{:.2f}".format(duration)})




def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
    
def runHttpServer():
    if is_port_in_use(HTTP_PORT):
        print('tools server already started.')
        return False
    # run(host='127.0.0.1', port=HTTP_PORT, debug=False)
    threading.Thread(daemon=True, target=run, 
                     kwargs={
                        'host':'127.0.0.1', 'port':HTTP_PORT, 'debug':False
                     }).start()

    return True


def openBrowser(app):

    def windows_getBrowserPath(browser='Edge'): # Chrome or  Edge
        edge_sufix = 'Microsoft\Edge\Application\msedge.exe'
        chrome_suffix = 'Google\Chrome\Application\chrome.exe'    
        
        suffix = edge_sufix if browser == 'Edge' else chrome_suffix
        
        Envfolders = [
            'LocalAppData',
            'ProgramFiles',
            'ProgramFiles(x86)',
        ]
        
        for ef in Envfolders:
            folder = os.environ.get(ef)
            if not folder:
                continue
            path = os.path.join(folder, suffix)
            if os.path.exists(path):
                return path
        
        print(f'{browser} not found!')
        return None


    appOpenOK = False
    if platform.system() == 'Windows':
        browserPath = windows_getBrowserPath('Edge')
        if browserPath is None :
            exit()
            
        # print(browserPath)

        try:    
            po = subprocess.Popen(
                [   browserPath, '--new-window', 
                    f'--app=http://127.0.0.1:{HTTP_PORT}/index.html#/{app}',
                    '-window-size=800,800',
                    '--window-position=0,0',
                    '--disable-application-cache',
                    '--incognito',
                    # f'''--user-data-dir="{os.environ['tmp']}/chrome_tmp_user_dir_23"'''
                ])
            appOpenOK = True
        except:
            pass

    if not appOpenOK:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{HTTP_PORT}/index.html#/{app}', 
                        new=1, 
                        autoraise=True)

def runTool(app):
    """

    Parameters
    ----------
    app : str
        app name, like 'androidtool' 
    """
    serverRunInThisTask = runHttpServer()

    openBrowser(app)

    if serverRunInThisTask:        
        while True:
            cmd = input()
            if cmd == 'exit':
                break