import ctypes
from .utils import convert_to_absolutes


INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

class MouseController:
    def __init__(self):
        self.SendInput = ctypes.windll.user32.SendInput

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
            ]

        class INPUT(ctypes.Structure):
            class _INPUT(ctypes.Union):
                _fields_ = [
                    ("mi", MOUSEINPUT)
                ]
            _anonymous_ = ("_input",)
            _fields_ = [
                ("type", ctypes.c_ulong),
                ("_input", _INPUT)
            ]

        self.INPUT = INPUT
        self.MOUSEINPUT = MOUSEINPUT

        self.screen_x, self.screen_y = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    def send_mouse_input(self, dx, dy, flag, time=0):
        _input = self.INPUT(
            type=self.INPUT_MOUSE,
            mi=self.MOUSEINPUT(
                dx=dx,
                dy=dy,
                mouseData=0,
                dwFlags=flag,
                time=time,
                dwExtraInfo=None
            )
        )

        self.SendInput(1, ctypes.byref(_input), ctypes.sizeof(_input))

    def move_absolute(self, x=0, y=0):
        absolute_x, absolute_y = convert_to_absolutes(
            dx=x,
            dy=y,
            screen_x=self.screen_x,
            screen_y=self.screen_y
        )

        self.send_mouse_input(
            dx=absolute_x,
            dy=absolute_y,
            flag=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        )

    def move_relative(self, x, y):
        self.send_mouse_input(
            dx=int(x * (self.screen_x / 1920)),
            dy=int(y * (self.screen_x / 1080)),
            flag=MOUSEEVENTF_MOVE
        )


    def left_click(self, x=0, y=0):
        # left mb down
        self.send_mouse_input(
            dx=x,
            dy=y,
            flag=MOUSEEVENTF_LEFTDOWN
        )

        # left mb up
        self.send_mouse_input(
            dx=x,
            dy=y,
            flag=MOUSEEVENTF_LEFTUP
        )

    def right_click(self, x=0, y=0):
        # right mb down
        self.send_mouse_input(
            dx=x,
            dy=y,
            flag=MOUSEEVENTF_RIGHTDOWN
        )

        # right mb up
        self.send_mouse_input(
            dx=x,
            dy=y,
            flag=MOUSEEVENTF_RIGHTUP
        )