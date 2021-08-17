import pyautogui
import PIL

def get_screen_shot():
    img = pyautogui.screenshot(region=[0, 0, 100, 100])  # x,y,w,h
    img.save('screenshot.png')  # PIL Image object
    # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)