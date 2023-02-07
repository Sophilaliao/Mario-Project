import numpy as np
from PIL import ImageGrab
import cv2
import time
import win32gui
import win32com.client
import keyboard
import ctypes

def screen_record(bbox): 
    #last_time = time.time()
    gameplay = list()
    while(True):
        # 800x600 windowed mode
        printscreen =  np.array(ImageGrab.grab(bbox)) #Left, Top, Right, Bottom
        #print('loop took {} seconds'.format(time.time()-last_time))
        #last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY))
        gameplay.append(printscreen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            gameplay = np.array(gameplay)
            gameplay_playback(gameplay)
            cv2.destroyAllWindows()
            break

def gameplay_playback(gameplay: list) -> None:
    for idx in range(len(gameplay)):
        cv2.imshow('record',cv2.cvtColor(gameplay[idx], cv2.COLOR_BGR2GRAY))
        cv2.waitKey(100)

def app_select(strWindows_name):
    bbox = list()
    window_ls= list()
    def enumhandler(hwnd, params):
        curr_window = win32gui.GetWindowText(hwnd)
        window_ls.append(curr_window)
        if strWindows_name in win32gui.GetWindowText(hwnd):
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.ShowWindow(hwnd, 9)
            win32gui.SetForegroundWindow(hwnd)
            #bbox.append(win32gui.GetWindowRect(hwnd))
            bbox.append(get_window_rect(hwnd))

    win32gui.EnumWindows(enumhandler,None)
    if len(bbox) == 0:
        print('Application Not Found')
        return False
    bbox = bbox[0]
    return bbox


def holdkey(hold_time,keyinput):
    start_time = time.time()
    while time.time() - start_time < hold_time:        
        keyboard.send(keyinput)

def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f: # Vista & 7 stuff
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
        )      
        return rect.left, rect.top, rect.right, rect.bottom


bbox = app_select('VisualBoyAdvance')
if bbox:
    screen_record(bbox)
