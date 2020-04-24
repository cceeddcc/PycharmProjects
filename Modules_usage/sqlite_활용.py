import sqlite3
import os
os.chdir("C:\\Users\\S\\Desktop")

# DB 생성 및 연결
conn = sqlite3.connect("test.db")
conn = sqlite3.connect(':memory:') # DB생성 안하고 메모리 기반으로 DB생성 가능
                                   # 프로그램이 종료되면 데이터가 유실됨

# 테이블 생성
cur = conn.cursor()
cur.execute("create table test (name text, score int)")


# 데이터 Insert
"""
반드시 commit 명령어를 사용해야 DB에 반영된다.
"""
cur.execute("insert into test values ('a', 100)")
conn.commit()
cur.execute("insert into test values (?, ?)", ('b', 1)) # tuple 형
conn.commit()
cur.execute("insert into test values (:name, :score)", {'name':'c', 'score':99}) # dict형
conn.commit()

# 여러 데이터 입력
"""
executemany 활용
"""
data = [
 ('d', 93),
 ('e', 11)
]
cur.executemany("insert into test values (?, ?)", data)
conn.commit()

# 데이터 Select
cur.execute('select * from test')
cur.fetchone() # 로우 단위 데이터 한줄씩 튜플로 반환
for row in cur:
    print(row)

cur.execute("select * from test")
rows = cur.fetchall() # 리스트로 한번에 가져오기
print(rows)

# 데이터 Update, Delete
cur.execute("update test set score=11 where name='b'")
conn.commit()

cur.execute("delete from test where name='e'")
conn.commit()

# DB 연결종료
conn.close()


# DataFrame 객체 sqlite db로 저장
from pandas import DataFrame
raw_data = {'col0': [1, 2, 3, 4], 'col1': [10, 20, 30, 40], 'col2':[100, 200, 300, 400]}
df = DataFrame(raw_data) ; df

con = sqlite3.connect("C:/Users/S/desktop/kospi.db")
df.to_sql('test', con) # test라는 이름의 테이블로 sql db로 저장


# DataFrame에 많은 로우가 있어서 패킷크기 제약으로 에러 발생 가능 이 경우 한 번에 데이터베이스로 저장될 로우의 개수를 지정
df.to_sql('test', con, chunksize=1000)


# Sqlite DB에서 DataFrame객체로 로드
import pandas as pd
con = sqlite3.connect("C:/Users/S/desktop/kospi.db")  # sqlite 연결 db 객체 생성
df = pd.read_sql("SELECT * FROM kakao", con, index_col=None) # SQLite DB 읽기
df
df = pd.read_sql("SELECT * FROM test", con, index_col='index')
df