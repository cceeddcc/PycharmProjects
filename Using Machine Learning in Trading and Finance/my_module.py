"""
자주 사용하는 code를 기록해 놓기 위함 
"""
import pandas as pd 

def road_codename():
    """
    KOSPI 종목명, 코드 불러오기 위함
    """
    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
        code_list = [line[1:].split("\n")[0] for line in f.readlines()]

    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f:
        name_list = [line.split("\n")[0] for line in f.readlines()]

    code_dict = {}
    for i in range(0, len(code_list)):
        code_dict["%s" % name_list[i]] = code_list[i]

    return code_dict, code_list, name_list
