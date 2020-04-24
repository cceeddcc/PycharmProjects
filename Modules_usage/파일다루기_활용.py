"""
r	읽기모드 - 파일을 읽기만 할 때 사용
w	쓰기모드 - 파일에 내용을 쓸 때 사용
a	추가모드 - 파일의 마지막에 새로운 내용을 추가 시킬 때 사용
"""

# csv파일로 저장
f = open('c:\\Users\\S\\Desktop\\kospi.csv', 'w')
for key, value in kospi.items():
    f.write("%s,%s\n" % (key, value))
f.close()


# with문 활용
with open("foo.txt", "w") as f:
    f.write("Life is too short, you need python")

"""
with문을 사용하면 with 블록을 벗어나는 순간 열린 파일 객체 f가 자동으로 close되어 편리하다.
"""