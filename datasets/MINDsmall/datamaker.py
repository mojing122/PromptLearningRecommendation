import pandas as pd
import numpy as np
import random
import csv
import os

random.seed(144)

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 3000)
behaviors = pd.read_csv('behaviors.tsv', sep='\t',
                   names=["IID", "UID", "Time", "History", "Impressions"])
news = pd.read_csv('news.tsv', sep='\t',
                   names=["NID", "Category", "SubCategory", "Title", "Abstract", "URL", "TEntities", "AEntities"], index_col="NID")


ft = open('all/train.csv', 'w', encoding='utf-8', newline='')
csv_writert = csv.writer(ft,delimiter='|')

fv = open('all/test.csv', 'w', encoding='utf-8', newline='')
csv_writerv = csv.writer(fv,delimiter='|')
ik = 0

for index, row in behaviors.iterrows():
    if(pd.isna(behaviors.loc[index,'History']) or pd.isna(behaviors.loc[index,'Impressions'])):
        continue
    His_list = behaviors.loc[index,'History'].split(" ")
    His_N_list = []
    for HisN in His_list:
        His_N_list.append(news.loc[HisN,"Title"])
    text_a = " [NSEP] ".join(His_N_list)
    IList = behaviors.loc[index,'Impressions'].split(" ")
    for v in IList:
        cN,i =v.split("-")
        OneRow = []
        OneRow.append(text_a)
        OneRow.append(news.loc[cN,"Title"])
        OneRow.append(i)
        ch_flag = random.randint(1, 10)
        if (ch_flag < 9):
            csv_writert.writerow(OneRow)
        else:
            csv_writerv.writerow(OneRow)
    ik += 1
    if ik > 1000:
        break
ft.close()
fv.close()

# movies=pd.read_csv('movies.csv')
# ratings=pd.read_csv('ratings.csv')
