import ctypes
from ctypes import wintypes

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004
MAPVK_VK_TO_VSC = 0

VK_RETURN = 0x0D

class KeyboardController:
    def __init__(self):
        wintypes.ULONG_PTR = wintypes.WPARAM

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = (("dx", wintypes.LONG),
                        ("dy", wintypes.LONG),
                        ("mouseData", wintypes.DWORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", wintypes.ULONG_PTR))

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = (("wVk", wintypes.WORD),
                        ("wScan", wintypes.WORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", wintypes.ULONG_PTR))

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if not self.dwFlags & KEYEVENTF_UNICODE:
                    self.wScan = ctypes.windll.user32.MapVirtualKeyW(self.wVk, MAPVK_VK_TO_VSC)

        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = (("uMsg", wintypes.DWORD),
                        ("wParamL", wintypes.WORD),
                        ("wParamH", wintypes.WORD))

        class INPUT(ctypes.Structure):
            class _INPUT(ctypes.Union):
                _fields_ = (("ki", KEYBDINPUT),
                            ("mi", MOUSEINPUT),
                            ("hi", HARDWAREINPUT))
            _anonymous_ = ("_input",)
            _fields_ = (("type", wintypes.DWORD),
                        ("_input", _INPUT))

        self.INPUT = INPUT
        self.KEYBDINPUT = KEYBDINPUT
        self.KEYEVENTF_KEYUP = KEYEVENTF_KEYUP

    def _get_vk_code(self, key):
        return ord(key.upper())

    def send_input(self, *input_keys):
        num_inputs = len(input_keys)
        lp_input = self.INPUT * num_inputs
        p_inputs = lp_input(*input_keys)
        cb_size = ctypes.c_int(ctypes.sizeof(self.INPUT))
        
        # actually type
        ctypes.windll.user32.SendInput(num_inputs, p_inputs, cb_size)

    def press_key(self, key):
        ki = self.KEYBDINPUT(wVk=self._get_vk_code(key=key))
        x = self.INPUT(type=INPUT_KEYBOARD, _input=self.INPUT._INPUT(ki=ki))
        self.send_input(x)

    def release_key(self, key):
        ki = self.KEYBDINPUT(wVk=self._get_vk_code(key=key), dwFlags=self.KEYEVENTF_KEYUP)
        x = self.INPUT(type=INPUT_KEYBOARD, _input=self.INPUT._INPUT(ki=ki))
        self.send_input(x)

    def write(self, input_str):
        for char in input_str:
            self.press_key(char)
            self.release_key(char)
