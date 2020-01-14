import os
"os 모듈은 Operating System의 약자로서 운영체제에서 제공되는 여러 기능을 파이썬에서 수행할 수 있게 해줍니다."
os.getcwd() # 현재 코드 실행 경로 확인
os.listdir(_) # 해당 경로에 해당하는 파일 및 디렉토리 리스트

# 사용 예시
for x in os.listdir('C:\\Users\\S\\Anaconda3'):
        if x.endswith('exe'): # 끝이 exe로 끝나는 파일만 출력
                print(x)