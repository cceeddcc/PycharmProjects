# 종목명, 코드 불러오기
with open("c:/Users/S/Desktop/code_list2.txt", "r") as f:
    code_list = [line.split("\n")[0] for line in f.readlines()]

code_list

