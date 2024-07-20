from sys import exit
import time
import pyautogui
from PIL import ImageGrab
import numpy as np

win = pyautogui.getWindowsWithTitle('Minecraft 1.7.10X - Mana Metal Mod 7.1.8')[0]
# win.activate()
time.sleep(3)
pyautogui.PAUSE = 0.0

im = pyautogui.screenshot()

# 找開始按鈕
startBtnX: int = 0
startBtnY: int = 0
for y in range(im.height-1, -1, -1):
    for x in range(im.width-1, -1, -1):
        r, g, b = im.getpixel((x, y))
        if (r, g, b) == (56, 116, 54):
            startBtnX = x
            startBtnY = y
            break
    else:
        continue
    break

print(startBtnX, startBtnY)

# 找左上角(整體的)
x1: int = 0
y1: int = 0

for y1 in range(im.height):
    for x1 in range(im.width):
        r, g, b = im.getpixel((x1, y1))
        if (r, g, b) == (128, 128, 128):
            # pyautogui.moveTo(x1, y1)
            break
    else:
        continue
    break

x2, y2 = x1, y1

# 過渡邊框
while pyautogui.pixelMatchesColor(x2, y2, (128, 128, 128)):
    y2 += 1
    x2 += 1
# 過渡到右下角(第一個單元格的)
while not pyautogui.pixelMatchesColor(x2, y2, (128, 128, 128)):
    y2 += 1
    x2 += 1

# 計算單元格大小
tileWidth = x2 - x1
tileHeight = y2 - y1

# 橫排12格，縱排5格
gameWidth = tileWidth * 12
gameHeight = tileHeight * 5

# 每格單元可拆成11*11的小格
unitWidth = tileWidth // 11
unitHeight = tileHeight // 11

print('tileWidth:', tileWidth, 'tileHeight:', tileHeight)
print('unitWidth:', unitWidth, 'unitHeight:', unitHeight)

# 點擊開始按鈕
pyautogui.click(startBtnX, startBtnY)
time.sleep(0.1)

now = time.time()

while True:
    im = ImageGrab.grab(bbox=(x1, y1, x1 + gameWidth, y1 + gameHeight))
    array = np.array(im.convert('L'))  # 轉成numpy array並灰階

    # 拆分成5*12個單元
    array = array.reshape((5, tileHeight, 12, tileWidth)).swapaxes(1, 2)
    array = array.reshape((-1, tileHeight, tileWidth))
    
    # 找出線斷掉的地方(255為白色, 128為灰色, 16為黑色)
    brokenStrings = np.where(array[:, 6*unitHeight, 5*unitWidth] < 100)[0]
    
    # 點擊線斷掉的地方
    for index in brokenStrings.tolist():
        if time.time() - now > 20:
            exit()
        
        relX = (index % 12) * tileWidth + 6 * unitWidth
        relY = (index // 12) * tileHeight + 6 * unitHeight
        pyautogui.moveTo(x1 + relX, y1 + relY, _pause=False)
        time.sleep(0.115)
        # time.sleep(0.12)       # 0.12s -> 190 score
        pyautogui.click()
        
        # pyautogui.click(x1 + relX, y1 + relY)