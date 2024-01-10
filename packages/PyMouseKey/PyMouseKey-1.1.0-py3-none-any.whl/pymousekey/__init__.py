import time
import math
import ctypes
import ctypes.wintypes
import threading

autoclickState = False
registered_hotkeys = {}
hotkey_threads = {}

PAUSE = 0.1
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP

LEFT = 'left'
RIGHT = 'right'
MIDDLE = 'middle'

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

WM_ACTIVATE = 0x6
WM_CHAR = 0x102
WA_ACTIVE = 0x1

WM_QUIT = 0x0012

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_LBUTTONCLICK = WM_LBUTTONDOWN + WM_LBUTTONUP
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_RBUTTONCLICK = WM_RBUTTONDOWN + WM_RBUTTONUP
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MBUTTONCLICK = WM_MBUTTONDOWN + WM_MBUTTONUP
WM_HOTKEY = 0x0312
WM_XBUTTONDOWN = 0x020B

WM_NCHITTEST = 0x0084
WM_MOUSEMOVE = 0x0200
WM_SETCURSOR = 0x0020

MK_LBUTTON = 0x0001
MK_MBUTTON = 0x0010
MK_RBUTTON = 0x0002

KEYS = {
    'escape': 0x01,
    'esc': 0x01,
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    'printscreen': 0xB7,
    'prntscrn': 0xB7,
    'prtsc': 0xB7,
    'prtscr': 0xB7,
    'scrolllock': 0x46,
    'pause': 0xC5,
    '`': 0x29,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    '-': 0x0C,
    '=': 0x0D,
    'backspace': 0x0E,
    'insert': 0xD2 + 1024,
    'home': 0xC7 + 1024,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    'numlock': 0x45,
    'divide': 0xB5 + 1024,
    'multiply': 0x37,
    'subtract': 0x4A,
    'add': 0x4E,
    'decimal': 0x53,
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1A,
    ']': 0x1B,
    '\\': 0x2B,
    'del': 0xD3 + 1024,
    'delete': 0xD3 + 1024,
    'end': 0xCF + 1024,
    'capslock': 0x3A,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    "'": 0x28,
    'enter': 0x1C,
    'return': 0x1C,
    'shift': 0x2A,
    'left shift': 0x2A,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    'right shift': 0x36,
    'ctrl': 0x1D,
    'left ctrl': 0x1D,
    'win': 0xDB + 1024,
    'winleft': 0xDB + 1024,
    'alt': 0x38,
    'left alt': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'spacebar': 0x39,
    'altright': 0xB8 + 1024,
    'winright': 0xDC + 1024,
    'apps': 0xDD + 1024,
    'right ctrl': 0x9D + 1024,
    'up arrow': ctypes.windll.user32.MapVirtualKeyW(0x26, 0),
    'left arrow': ctypes.windll.user32.MapVirtualKeyW(0x25, 0),
    'down arrow': ctypes.windll.user32.MapVirtualKeyW(0x28, 0),
    'right arrow': ctypes.windll.user32.MapVirtualKeyW(0x27, 0),
}

VK_KEYS = {
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4a,
    "k": 0x4b,
    "l": 0x4c,
    "m": 0x4d,
    "n": 0x4e,
    "o": 0x4f,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5a,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "0": 0x30,
    "-": 0xbd,
    "=": 0xbb,
    "!": 0x131,
    "@": 0x132,
    "#": 0x133,
    "$": 0x134,
    "%": 0x135,
    "^": 0x136,
    "&": 0x137,
    "*": 0x138,
    "(": 0x139,
    ")": 0x130,
    "_": 0x1bd,
    "+": 0x1bb,
    "[": 0xdb,
    "]": 0xdd,
    "\\": 0xdc,
    "{": 0x1db,
    "}": 0x1dd,
    "|": 0x1dc,
    ";": 0xba,
    "'": 0xde,
    ":": 0x1ba,
    '"': 0x1de,
    ",": 0xbc,
    ".": 0xbe,
    "/": 0xbf,
    "<": 0x1bc,
    ">": 0x1be,
    "?": 0x1bf,
    "*": 0x138,
    "`": 0xc0,
    "~": 0x1c0,
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps': 0x14,
    'spacebar': 0x20,
    'space bar': 0x20,
    'page up': 0x21,
    'page down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left arrow': 0x25,
    'up arrow': 0x26,
    'right arrow': 0x27,
    'down arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print screen': 0x2C,
    'prt sc': 0x2C,
    'prntsc': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    'numpad 0': 0x60,
    'numpad 1': 0x61,
    'numpad 2': 0x62,
    'numpad 3': 0x63,
    'numpad 4': 0x64,
    'numpad 5': 0x65,
    'numpad 6': 0x66,
    'numpad 7': 0x67,
    'numpad 8': 0x68,
    'numpad 9': 0x69,
    'multiply': 0x6A,
    'minus': 0xBD,
    'seperator': 0x6C,
    'subtract': 0x6D,
    'decimal': 0x6E,
    'divide': 0x6F,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
    'f13': 0x7C,
    'f14': 0x7D,
    'f15': 0x7E,
    'f16': 0x7F,
    'f17': 0x80,
    'f18': 0x81,
    'f19': 0x82,
    'f20': 0x83,
    'f21': 0x84,
    'f22': 0x85,
    'f23': 0x86,
    'f24': 0x87,
    'num lock': 0x90,
    'scroll lock': 0x91,
    'lshift': 0xA0,
    'rshift': 0xA1,
    'lcontrol': 0xA2,
    'lctrl': 0xA2,
    'rcontrol': 0xA3,
    'rctrl': 0xA3,
    'lalt': 0xA4,
    'ralt': 0xA5,
    'tilde': 0xC0,
    'clear': 0xFE,
}


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def getPos():
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return cursor.x, cursor.y

def size():
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    return screen_width, screen_height


def dragTo(x=None, y=None, duration=0.0, _pause=True):
    """
    Performs a drag (mouse movement with mouse button down) to coordinates on screen\n
    
    x,y(int): are the coordinates your going to drag to from your current cursor position\n
    
    Duration(int/float): is the time inbetween each mouse movement towards the new x & y coordinates, if 0 it moves almost instantly\n
    
    _pause is the sleep after every function call
    """

    start_x, start_y = getPos()
    screen_width, screen_height = size()
    duration = duration / 100

    distance = math.hypot(x - start_x, y - start_y)

    ii_ = Input_I()
    
    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(ctypes.c_ulong(0)))
    xx = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
    if _pause:
        time.sleep(PAUSE)

    for i in range(1, int(distance)+1):
        drag_x = int(start_x + (x - start_x) * i / int(distance))
        drag_y = int(start_y + (y - start_y) * i / int(distance))
        
        ii_.mi = MouseInput(int(65535 * drag_x / screen_width), int(65535 * drag_y / screen_height), 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, ctypes.pointer(ctypes.c_ulong(0)))
        xx = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
        if duration > 0.0:
            time.sleep(duration)

    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(ctypes.c_ulong(0)))
    xx = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
    if _pause:
        time.sleep(PAUSE)


def moveTo(x=None, y=None, _pause=True):
    """
    Moves the mouse to the specified x and y coordinates\n
    x,y(int): The coordinates your going to move to\n
    _pause is the sleep after every function call
    
    """
    screen_width, screen_height = size()
    ii_ = Input_I()
    ii_.mi = MouseInput(int(65535 * x / screen_width), int(65535 * y / screen_height), 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, ctypes.pointer(ctypes.c_ulong(0)))
    xx = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
    if _pause:
        time.sleep(PAUSE)


def moveRel(offsetX=0, offsetY=0, _pause=True):
    """
    Moves the mouse by a certain amount based off the x and y offsets\n
    offsetX,offsetY(int): The amount of pixels your going to move\n
    _pause is the sleep after every function call
    
    """

    x, y = getPos()
    moveTo(offsetX + x, offsetY + y, _pause)


def click(x=None, y=None, interval=0.0, clicks=1, button=LEFT, _pause=True):
    """
    Performs a mouse click at the specified x and y coordinates\n
    If no x and y coordinates are specified perform a mouse click at your mouse location\n
    x,y(int): The coordinates your going to move to\n
    interval(float): The sleep after the mouse key has been pressed so you can set your own intervals per call\n
    clicks(int): The amount of clicks you want to perform\n
    _pause is the sleep after every function call
    
    """
    if x and y:
        moveTo(x,y)

    if button == LEFT:
        event = MOUSEEVENTF_LEFTCLICK
    elif button == RIGHT:
        event = MOUSEEVENTF_RIGHTCLICK
    elif button == MIDDLE:
        event = MOUSEEVENTF_MIDDLECLICK

    ii_ = Input_I()
    for i in range(clicks):
        if x and y:
            ii_.mi = MouseInput(x,y, 0, event, 0, ctypes.pointer(ctypes.c_ulong(0)))
        else:
            ii_.mi = MouseInput(0,0, 0, event, 0, ctypes.pointer(ctypes.c_ulong(0)))
        xx = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
        time.sleep(interval)

    if _pause:
        time.sleep(PAUSE)


def autoclick(button=LEFT):
    """
    Starts a auto clicker in a seperate daemon thread at your current mouse location and clicks the specified button at roughly 200cps\n
    USE WITH CAUTION:
    -----
    Make sure you can call this function with a hotkey or another way because it will not automatically toggle off\n

    """
    global autoclickState
    autoclickState = not autoclickState
    def autoclick():
        while autoclickState:
            click(None, None, 0.004, 1, button, False)
    if autoclickState:
        autoclick_thread = threading.Thread(target=autoclick)
        autoclick_thread.daemon = True
        autoclick_thread.start()


def doubleClick(x=None, y=None, interval=0.0, button=LEFT, _pause=True):
    click(x, y, interval, 2, button, _pause)

def tripleClick(x=None, y=None, interval=0.0, button=LEFT, _pause=True):
    click(x, y, interval, 3, button, _pause)


def scroll(scrollAmount=1):
    """
    Sends a scroll input\n
    scrollAmount(int)\n
    _pause is the sleep after every function call\n
    Positive numbers scroll upwards, negative numbers scroll downwards\n

    Sometimes games dont take the scroll data that gets sent and just takes thes scroll input to scroll at a fixed amount
    
    """
    ii_ = Input_I()
    ii_.mi = MouseInput(0,0, scrollAmount*120, MOUSEEVENTF_WHEEL, 0, ctypes.pointer(ctypes.c_ulong(0)))
    xx = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))


def press(key, interval=0.0, _pause=True):
    """
    Performs a keypress, also supports side mouse buttons (xbutton1 and xbutton2)\n
    Key(string): The key/mouse button expected to be pressed\n
    interval(float): The sleep after the key has been pressed so you can set your own intervals per call\n
    _pause is the sleep after every function call\n
    pymousekey.KEYS for the dict of keys

    """
    if not key.lower() in KEYS or KEYS[key.lower()] is None:
        return
    ii_ = Input_I()
    
    if key == ('xbutton1' or 'xbutton2'):
        ii_.mi = MouseInput(0, 0, KEYS[key], MOUSEEVENTF_XDOWN | MOUSEEVENTF_XUP, 0, None)
        xx = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(xx), ctypes.sizeof(xx))
        return
    
    if str(key).isupper():
        ii_.ki = KeyBdInput(0, KEYS['shift'], KEYEVENTF_SCANCODE, 0, ctypes.pointer(ctypes.c_ulong(0)))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    keyDown(key)
    time.sleep(interval)
    keyUp(key)
    
    if str(key).isupper():
        ii_.ki = KeyBdInput(0, KEYS['shift'], KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(ctypes.c_ulong(0)))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    if _pause:
        time.sleep(PAUSE)


def keyDown(key):
    if not key.lower() in KEYS or KEYS[key.lower()] is None:
        return

    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, KEYS[key.lower()], KEYEVENTF_SCANCODE, 0, ctypes.pointer(ctypes.c_ulong(0)))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def keyUp(key):
    if not key.lower() in KEYS or KEYS[key.lower()] is None:
        return

    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, KEYS[key.lower()], KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(ctypes.c_ulong(0)))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def add_hotkey(key, callback, args=(), suppress=True):
    """
    Registers a system wide hotkey with optional args using ctypes and GetMessageW starting it in a seperate daemon thread\n
    If suppress is true then block the original function of the key\n
    If the specified key is already a registered hotkey the function returns nothing\n
    Usage of how to add hotkeys:
    -
    add_hotkey("ctrl + shift + g")\n
    add_hotkey("shift + numpad 5") (shift + numpad keys dont actually work because of something to do with numlock and its secondary function i have no clue)\n
    add_hotkey("h")\n
    """
    def add_hotkey_thread():
        if 'shift' in key or 'ctrl' in key or 'alt' in key:
            registered_key = key.rsplit('+', 1)[1].strip()
            key_id = len(registered_hotkeys) + 1
            registered_hotkeys[key] = key_id, VK_KEYS[registered_key]
            hotkey_threads[key] = hotkey_thread.native_id
            if 'alt' in key and not 'ctrl' in key and not 'shift' in key:
                fsModifiers = 0x0001
            elif 'ctrl' in key and not 'alt' in key and not 'shift' in key:
                fsModifiers = 0x0002
            elif 'shift' in key and not 'ctrl' in key and not 'alt' in key:
                fsModifiers = 0x0004
            elif 'alt' in key and 'ctrl' in key:
                fsModifiers = 0x0001 | 0x0002
            elif 'alt' in key and 'shift' in key:
                fsModifiers = 0x0001 | 0x0004
            elif 'shift' in key and 'ctrl' in key:
                fsModifiers = 0x0004 | 0x0002
        else:
            registered_key = key
            key_id = len(registered_hotkeys) + 1
            registered_hotkeys[key] = key_id, VK_KEYS[registered_key]
            hotkey_threads[registered_key] = hotkey_thread.native_id
            fsModifiers = None

        ctypes.windll.user32.RegisterHotKey(None, key_id , fsModifiers, VK_KEYS[registered_key])
        
        msg = ctypes.wintypes.MSG()

        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
            if msg.message == WM_HOTKEY:
                if args:
                    callback(args)
                else:
                    callback()
                if not suppress:
                    ctypes.windll.user32.UnregisterHotKey(None, key_id , fsModifiers, VK_KEYS[registered_key])
                    press(key, 0, False)
                    ctypes.windll.user32.RegisterHotKey(None, key_id , fsModifiers, VK_KEYS[registered_key])
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
        try:
            ctypes.windll.user32.UnregisterHotKey(None, registered_hotkeys[key][0])
        except(KeyError):
            pass
    try:
        if key in registered_hotkeys:
            return
    
        elif key in VK_KEYS:
            hotkey_thread = threading.Thread(target=add_hotkey_thread)
            hotkey_thread.daemon = True
            hotkey_thread.start()

        elif key.rsplit('+', 1)[1].strip() in VK_KEYS:
            hotkey_thread = threading.Thread(target=add_hotkey_thread)
            hotkey_thread.daemon = True
            hotkey_thread.start()
    except:
        pass

def remove_hotkey(key):
    """
    Unregisters and removes the specified hotkey if it was previously registered

    """
    if key in registered_hotkeys:
        ctypes.windll.user32.UnregisterHotKey(None, registered_hotkeys[key][0])
        ctypes.windll.user32.PostThreadMessageW(hotkey_threads[key], WM_QUIT, 0, 0)
        del registered_hotkeys[key]
        del hotkey_threads[key]

def remove_all_hotkeys():
    """
    Unregisters and removes all currently registered hotkeys
    
    """
    for key in registered_hotkeys.values():
        ctypes.windll.user32.UnregisterHotKey(None, key[0])
        
    for threads in hotkey_threads.values():
        ctypes.windll.user32.PostThreadMessageW(threads, WM_QUIT, 0, 0)

    registered_hotkeys.clear()
    hotkey_threads.clear()

def typeWrite(message, interval=0.0, _pause=True):
    """
    Types out a given message, letters suppors lowercase and uppercase letters\n
    message(str): The message you want typed out\n
    interval(float): The sleep after the key has been pressed so you can set your own intervals per call\n
    _pause is the sleep after every function call

    """
    for i in message:
        press(i, interval, _pause)


def getPixelColor(x=None, y=None):
    """
    Gets the color from the specified coordinates, if no coordinates are specified grab the color from your mouse coordinates\n
    Returns:
    ----
    hexColor & rgbColor
    
    """
    dc = ctypes.windll.user32.GetDC(None)
    if not (x and y):
        x,y = getPos()
        color = ctypes.windll.gdi32.GetPixel(dc, x, y)
    else:
        color = ctypes.windll.gdi32.GetPixel(dc, x, y)

    ctypes.windll.user32.ReleaseDC(None, dc)
    red = color & 0xff
    green = (color >> 8) & 0xff
    blue = (color >> 16) & 0xff
    hexColor = '#{:02x}{:02x}{:02x}'.format(red,green,blue)
    rgbColor = red, green, blue
    return hexColor, rgbColor


def controlSend(key=None, className=None, windowTitle=None, lparam=None):
    """
    Sends software keyboard inputs to any inactive window/control by sending the WM_ACTIVATE msg and WA_ACTIVE wParam then sending the WH_CHAR message with the key you specified\n
    
    Note:
    -------
    Some games/windows only take the hardware inputs as an option so if you dont see any results this is why

    """
    handle = ctypes.windll.user32.FindWindowW(className, windowTitle)

    ctypes.windll.user32.PostMessageW(handle, WM_ACTIVATE, WA_ACTIVE, 0)
    ctypes.windll.user32.PostMessageW(handle, WM_CHAR, ord(key), lparam)


def controlClick(x=None, y=None, className=None, windowTitle=None, button='left'):
    """
    Sends software mouse inputs to any inactive window/control by sending the WM_ACTIVATE msg and WA_ACTIVE wParam then sending WM_LBUTTONDOWN and WM_LBUTTONUP messages\n
    
    Note:
    -------
    Some games/windows ignore your lparam in PostMessageW and they instead use the return from GetPhysicalCursorPos instead\n

    Example: every game made with the unity game engine uses GetPhysicalCursorPos to determine were the user has clicked\n

    """

    handle = ctypes.windll.user32.FindWindowW(className, windowTitle)
    lparam = ctypes.c_long((y << 16) | (x & 0xFFFF)).value

    ctypes.windll.user32.PostMessageW(handle, WM_ACTIVATE, WA_ACTIVE, 0)
    
    if button == 'left':
        ctypes.windll.user32.PostMessageW(handle, WM_NCHITTEST, 0, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_LBUTTONDOWN, MK_LBUTTON, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_LBUTTONUP, MK_LBUTTON, lparam)

    elif button == 'right':
        ctypes.windll.user32.PostMessageW(handle, WM_NCHITTEST, 0, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_RBUTTONDOWN, MK_RBUTTON, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_RBUTTONUP, MK_RBUTTON, lparam)

    elif button == 'middle':
        ctypes.windll.user32.PostMessageW(handle, WM_NCHITTEST, 0, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_MBUTTONDOWN, MK_MBUTTON, lparam)
        ctypes.windll.user32.PostMessageW(handle, WM_MBUTTONUP, MK_MBUTTON, lparam)