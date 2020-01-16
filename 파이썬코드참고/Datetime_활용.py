from datetime import datetime


# String, Date 변환
# string format time : time -> string
datetime.strftime(datetime.now(), "%Y-%m-%d")

# string parse time : string -> time
datetime.strptime("20200105", "%Y%m%d")