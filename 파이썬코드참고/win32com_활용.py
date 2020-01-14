import win32com.client

"""
프로그래밍 언어와 관계없이 개발된 객체를 사용하는 방법
COM (Component Object Model) : 다른 언어로 개발된 Component들을 객체로 Python코드 내에서 객체로 만들어 사용하는 모델을 의미한다.
"""
explore = win32com.client.Dispatch("InternetExplorer.Application") # 인터넷익스플로어를 객체로 생성하여 사용
explore.Visible = True

word = win32com.client.Dispatch("Word.Application") # 워드를 객체로 생성하여 사용
word.Visible = True