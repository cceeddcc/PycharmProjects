import pyautogui
import time
pyautogui.FAILSAFE = True #(False 값을 넣을 경우 오류 발생시 실행 멈추지 않음)
pyautogui.position()
f = open('c:\\Users\\S\\Desktop\\code_list.txt', 'r')
lines = f.readlines()
code_list = []
for line in lines:
        nline = line.split('\n')[0]
        code_list.append(nline)

# code_list = missingcode # for test
i = 1
for code_name in code_list:
    print(i,"/", len(code_list))
    i += 1
    pyautogui.click(x=113, y=181)
    time.sleep(0.2)
    pyautogui.click(x=254, y=302)
    pyautogui.typewrite(code_name)
    time.sleep(0.5)
    pyautogui.doubleClick(x=190, y=351)
    time.sleep(0.5)
    pyautogui.click(x=368, y=354, button='right')
    time.sleep(0.2)
    pyautogui.click(x=411, y=601)
    time.sleep(0.2)
    pyautogui.typewrite(code_name)
    time.sleep(0.5)
    pyautogui.click(x=757, y=594)
    time.sleep(0.5)

#
# # missing code 찾기 !
# import os
# # os.getcwd() # 현재 코드 실행 경로 확인
# # os.listdir(_) # 해당 경로에 해당하는 파일 및 디렉토리 리스트
# #
# # 사용예시
# mylist = os.listdir('C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무')
# mylist2 = []
# for x in mylist :
#     mylist2.append(x.split(".")[0])
#
# missingcode =[]
# for test in code_list:
#     if not test in mylist2 :
#         missingcode.append(test)
#
