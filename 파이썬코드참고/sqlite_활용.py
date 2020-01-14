import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/kospi.db")  # sqlite 연결 db 객체 생성
print(type(con))
sqlite3.Connection # 연결

cursor = con.cursor() # db 객체를 이용하기 위한 컨트롤용 객체 생성

# SQL 구문 실행
cursor.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)") # SQL구문 실행
cursor.execute("INSERT INTO kakao VALUES('16.06.03', 97000, 98600, 96900, 98000, 321405)") # kakao테이블에 데이터 입력
cursor.execute("INSERT INTO kakao VALUES('16.06.02', 99000, 99300, 96300, 97500, 556790)")

con.commit() # 데이터베이스에 반영
con.close() # db 종료

# sqlite db데이터 가져오기
con = sqlite3.connect("C:/Users/S/desktop/kospi.db")  # sqlite 연결 db 객체 생성
cursor = con.cursor()
cursor.execute("SELECT * FROM kakao") # kakao table에서 모두 가져오기
cursor.fetchone() # 로우 단위 데이터 한줄씩 튜플로 반환

cursor.execute("SELECT * FROM kakao")
cursor.fetchall() # 로우 단위로 모든 데이터 가져오기

cursor.execute("SELECT * FROM kakao")
kakao = cursor.fetchall()
kakao[0][0] # 인덱싱으로 데이터 추출
kakao[0][1]

# DataFrame 객체 sqlite db로 저장
import pandas as pd
from pandas import Series, DataFrame
raw_data = {'col0': [1, 2, 3, 4], 'col1': [10, 20, 30, 40], 'col2':[100, 200, 300, 400]}
df = DataFrame(raw_data)
df


import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/kospi.db")  # sqlite 연결 db 객체 생성
df.to_sql('test', con) # test라는 이름의 테이블로 sql db로 저장

# DataFrame에 많은 로우가 있어서 패킷크기 제약으로 에러 발생 가능 이 경우 한 번에 데이터베이스로 저장될 로우의 개수를 지정
df.to_sql('test', con, chunksize=1000)

# Sqlite DB에서 DataFrame객체로 로드
import pandas as pd
from pandas import Series, DataFrame
import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/kospi.db")  # sqlite 연결 db 객체 생성
df = pd.read_sql("SELECT * FROM kakao", con, index_col=None) # SQLite DB 읽기
df
df = pd.read_sql("SELECT * FROM test", con, index_col='index')
df