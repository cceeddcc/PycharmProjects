import pyautogui
import pandas as pd
import time

df= pd.read_excel("C:/Users/S/Desktop/종목명.xlsx")
df
for i in range(0,len(df["종목명"])) :
    print(df.iloc[i,0])

pyautogui.position()
pyautogui.moveTo(200, 200, 2)
pyautogui.doubleClick(x=200, y=200)
pyautogui.press('enter')
pyautogui.dragTo(x=100
                 , y=100)
time.sleep(0.2)
pyautogui.doubleClick(x=621, y=165)
pyautogui.click(x=366, y=703,button='right')
pyautogui.click(x=366, y=703,button='right')
pyautogui.click(x=366, y=703,button='right')
pyautogui.typewrite(df.iloc[1,0])
time.sleep(0.2)
pyautogui.click(x=424, y=335)
pyautogui.click(x=679, y=378)
