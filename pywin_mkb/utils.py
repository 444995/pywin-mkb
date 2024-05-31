def convert_to_absolute_coords(dx, dy, screen_x, screen_y):
    return (int(65536 * dx / screen_x), 
            int(65536 * dy / screen_y))

def convert_to_relative_coords(dx, dy, screen_x, screen_y):
    return (int(dx * (screen_x / 1920)), 
            int(dy * (screen_y / 1080)),)