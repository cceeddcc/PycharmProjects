import pandas as pd
import sqlite3 as sql
import shutil
import os
import time
import networkx as nx

doc = """ 
example :

# read brain
df_edlist, df_know = brain.load_brain()

# modify brain
brain.mod_brain(df_edlist,df_know)

# save_brain()
brain.save_brain()


# visualization
brain.visualize_brain(df_edlist[df_edlist["n1"]=="invertibility"])

"""


# path
file_path = "C:/Users/S/PycharmProjects/knowledge_associating/"
backup_path = "C:/Users/S/PycharmProjects/knowledge_associating/backup/"

def load_brain():
    """
    return knowledgelist, edgelist dataframe
    initialize backupfile and load brain db
    """
    # backup file 생성
    if len(os.listdir(backup_path)) >= 20 :
        os.remove(backup_path+"%s" %os.listdir(backup_path)[0])
    timestamp = time.strftime("%Y%m%d%H%M%S",time.localtime())
    shutil.copyfile(file_path+"brain.db", backup_path+"brain_%s.db" %timestamp)

    # brain db 불러오기
    con = sql.connect(file_path+"brain.db")
    df_edlist = pd.read_sql("SELECT * FROM edgelist", con, index_col=None)
    df_know = pd.read_sql("SELECT * FROM knowledgelist", con, index_col=None)
    con.close()

    print("brain db를 성공적으로 불러왔습니다.")

    return df_edlist, df_know


def mod_brain(df_edlist,df_know):
    """
    open brain file to modify brain db
    """
    print("brain 수정을 시작합니다. 수정을 마친 후 꼭 저장해 주세요.")
    df_edlist.to_excel(file_path + "edgelist.xlsx", index=None)
    df_know.to_excel(file_path + "knowledgelist.xlsx", index=None)
    os.startfile(file_path + "knowledgelist.xlsx")
    os.startfile(file_path + "edgelist.xlsx")


def save_brain():
    """
    save the modified db to sql
    """
    df_know_new = pd.read_excel(file_path+"knowledgelist.xlsx",index_col=None)
    df_edlist_new = pd.read_excel(file_path+"edgelist.xlsx",index_col=None)

    # remove old db and make new db
    os.remove(file_path+"brain.db")
    con = sql.connect(file_path+"brain.db")
    df_know_new.to_sql("knowledgelist", con, index=None)
    df_edlist_new.to_sql("edgelist", con, index=None)
    con.close()

    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print("성공적으로 저장하였습니다. %s" %timestamp)


def visualize_brain(df_edlist):
    """
    visualizing the brain
    """
    G = nx.from_pandas_edgelist(df_edlist, 'n1', 'n2', edge_attr='relation')
    nx.draw(G, with_labels=1)



