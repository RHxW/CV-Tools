import win32api, win32con, win32gui
def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle)
x1, y1, x2, y2 = get_window_pos('暴雪战网')
print(x1,y1,x2,y2)