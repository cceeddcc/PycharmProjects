import win32com.client
import pandas as pd
import os

__doc__ = """
RQ(request) 제한
시세오브젝트 : 15초에최대 60건으로제한, 
초과요청시 첫 요청으로부터 15초가 지날 때 까지 내부적으로 기다림

주문관련오브젝트 : 15초에최대 20건으로제한,
초과요청시 첫 요청으로부터 15초가 지날 때 까지 
요청함수(Request, BlockRequest, BlockRequest2)에서 4를반환

SB(subscibe) 제한
시세오브젝트 : 최대 400건의요청으로제한, 초과요청시오류
주문관련오브젝트 : 제한없음

위의제한사항은당사방침에따라변경될수있습니다.
"""

class CP_Util :

    def __init__(self):
        self.CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.CP_login_status()

    def CP_login_status(self):
        """
        check CP login status
        """

        if self.CpCybos.IsConnect == 1: # 1: connected , 0: disconnected
            print("CP is connected")
            return True
        else:
            print("CP is disconnected")
            return False

    @staticmethod
    def login_CP():
        os.startfile("C:\\Users\\S\\Desktop\\CybosPlus.lnk")
        print("CybosPlus.exe을 실행합니다.")