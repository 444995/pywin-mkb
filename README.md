# pywin-mouse
pywin-mouse allows you to control the mouse on Windows extremely easily - it leverages *pywin32*, specifically SendInput, so it's blazingly fast.

## Usage
Here is an example of how to use pywin-mouse:
```
from pywin_mouse import MouseController

# Initialize the MouseController
mouse = MouseController()

# Move the mouse to an absolute position (e.g., top-left corner of the screen)
mouse.move_absolute(x=0, y=0)

# Move the mouse relative to its current position (e.g., move 100 pixels right and 50 pixels down)
mouse.move_relative(x=100, y=50)

# Perform a left click at the current mouse position
mouse.left_click()

# Perform a right click at the current mouse position
mouse.right_click()

```

## Installation
To install, clone the repository and install it using *pip*:
```
git clone https://github.com/oliver748/pywin-mouse
cd pywin-mouse
pip install .
```