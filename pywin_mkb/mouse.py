import ctypes
from .utils import convert_to_absolute_coords, convert_to_relative_coords


INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

class Button:
    left = 0
    right = 1
    middle = 2

class MouseController:
    def __init__(self):
        self.SendInput = ctypes.windll.user32.SendInput

        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

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
        self.POINT = POINT

        self.screen_x, self.screen_y = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    def _get_current_mouse_pos(self):
        cursor = self.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        return cursor

    def send_mouse_input(self, dx, dy, flag, time=0):
        _input = self.INPUT(
            type=INPUT_MOUSE,
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
        absolute_x, absolute_y = convert_to_absolute_coords(
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
        relative_x, relative_y = convert_to_relative_coords(
            dx=x,
            dy=y,
            screen_x=self.screen_x,
            screen_y=self.screen_y
        )

        self.send_mouse_input(
            dx=relative_x,
            dy=relative_y,
            flag=MOUSEEVENTF_MOVE
        )


    def press_button(self, button):
        if button == Button.left:
            self.send_mouse_input(0, 0, MOUSEEVENTF_LEFTDOWN)
        elif button == Button.right:
            self.send_mouse_input(0, 0, MOUSEEVENTF_RIGHTDOWN)
        
    def release_button(self, button):
        if button == Button.left:
            self.send_mouse_input(0, 0, MOUSEEVENTF_LEFTUP)
        elif button == Button.right:
            self.send_mouse_input(0, 0, MOUSEEVENTF_RIGHTUP)


    def click(self, button, x=None, y=None):
        """click func moves absolute to x, y; not relative"""

        # makes sure that user can for example only pass x=200 without specifying y
        if x is None:
            x = self._get_current_mouse_pos().x
        if y is None:
            y = self._get_current_mouse_pos().y
        
        self.move_absolute(x=x, y=y)
        
        self.press_button(button=button)
        self.release_button(button=button)


