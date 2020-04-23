import os
"""
os 모듈은 Operating System의 약자로서 운영체제에서 제공되는 여러 기능을
파이썬에서 수행할 수 있게 해줍니다.
"""

dir(os) # os와 관련된 attribute, module명 확인

# 현재 작업 경로 확인
os.getcwd() #  get current working directory
os.chdir("C:/Users/S/Desktop/바탕화면(임시)/프로그래밍") # change directory
os.getcwd()

os.listdir() # 해당 경로에 해당하는 파일 및 디렉토리 리스트
for x in os.listdir('C:\\Users\\S\\Anaconda3'):
        if x.endswith('exe'): # 끝이 exe로 끝나는 파일만 출력
                print(x)

# 폴더 생성
os.mkdir("Demo1") # make directory
os.mkdir("Demo2/subDemo") # 오류 : 아직 생성되지 않은 dir에 sub dir 생성 불가
os.makedirs("Demo2/subDemo") # mkdir과 비슷하지만 더 deep한 기능

# 폴더 삭제
os.rmdir("Demo1") # remove directory
os.rmdir("Demo2/subDemo") # remove directory
os.removedirs("Demo2/subDemo") # rmdir과 비슷하지만 더 deep한 기능, 상위 폴더, 하위폴더까지 모두 삭제
os.listdir()

# 폴더명 변경
os.rename("test.txt", "demo.txt") # test.txt -> demo.txt 변경

os.stat("demo.txt")
os.stat("demo.txt").st_size # 파일크기 확인
os.stat("demo.txt").st_mtime # 최종수정날짜

from datetime import datetime
mod_time = os.stat("demo.txt").st_mtime
datetime.fromtimestamp((mod_time)) # timestamp확인

# os.walk
"""
해당 폴더 내의 모든 폴더 및 하위폴더까지 순차적으로 접근함 
"""
for dirpath, dirnames, filenames in os.walk("C:/Users/S/Desktop/바탕화면(임시)/프로그래밍") :
        print(dirpath)
        print(dirnames)
        print(filenames)
        print()


# os.path
"""
경로 관련 
"""
file_path= os.path.join("C:/Users/S/Desktop/바탕화면(임시)/프로그래밍","test.txt") # 경로 결합
with open(file_path, "w") as f:
        f.write("haha")

os.path.basename(file_path) # 경로 최종명
os.path.dirname(file_path) # 경로 중간명
os.path.split(file_path) # 경로의 중간과 최종을 분리
os.path.exists(file_path) # 해당 경로가 존재하는지 확인 T/F
os.path.isdir(file_path) # dir인지 확인
os.path.isfile(file_path) # file인지 확인
os.path.splitext(file_path) # 파일명과 확장자 분리
print(dir(os.path)) # os.path 메서드, 속성 모두 확인 가능

# 파일, application 실행
os.startfile("'C:\\Users\\S\\Desktop\\CybosPlus.lnk")
# cf import subprocess랑 비교