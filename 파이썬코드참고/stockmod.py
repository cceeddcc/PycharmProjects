"""
모듈 생성 연습용
"""

def cal_upper_lower(price):
    upper_price = price * 1.3
    lower_price = price * 0.7
    return (upper_price,lower_price)

author = "harim"

if __name__ == "__main__" : # 모듈 내에서 함수가 제대로 작동하는지 test하기 위함
    print(cal_upper_lower(10000))
    print(__name__)