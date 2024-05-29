def convert_to_absolutes(dx, dy, screen_x, screen_y):
    return (int(65536 * dx / screen_x), 
            int(65536 * dy / screen_y))
