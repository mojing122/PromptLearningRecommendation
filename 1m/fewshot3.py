import pandas as pd
import numpy as np
import random
import csv
import os
random.seed(144)

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 3000)
movies=pd.read_csv('1movies.dat',sep='::',names=['movieId','title','genres'],encoding='ISO-8859-1')
ratings=pd.read_csv('1ratings.dat',sep='::',names=['userId','movieId','rating','timestamp'],encoding='ISO-8859-1')
#movies=pd.read_csv('movies.csv')
#ratings=pd.read_csv('ratings.csv')


#label=['adore','love','like','dislike','hate']
label=['great','good','common','bad','awfully']
data = pd.merge(ratings,movies,on='movieId')

data.insert(3,'mood',None)
a=set(data['userId'])

for uid in a:
    train = []
    test = []
    datai=data[data.userId==uid]
    b = datai.index.tolist()
    random.shuffle(b)
    length = 10
    if len(b)<length*5:
        continue
    for index, row in datai.iterrows():
        if (5 >= float(row['rating']) > 4):
            datai.loc[index, 'mood'] = 'great'
        elif (4 >= float(row['rating']) > 3):
            datai.loc[index, 'mood'] = 'good'
        elif (3 >= float(row['rating']) > 2):
            datai.loc[index, 'mood'] = 'common'
        elif (2 >= float(row['rating']) > 1):
            datai.loc[index, 'mood'] = 'bad'
        else:
            datai.loc[index, 'mood'] = 'awfully'
    flag=0
    for lab in label:
        #print(len(datai[datai.mood==lab]))
        if len(datai[datai.mood==lab])<length:
            flag=1
    if flag==1:
        continue
    for lab in label:
        count=0
        datal=datai[datai.mood==lab]
        for index, row in datal.iterrows():
            example = []
            labeli = label.index(datal.loc[index, 'mood']) + 1
            example.append(labeli)
            example3 = ' '.join(datal.loc[index, 'genres'].split("|"))  + ' movie ' +datal.loc[index, 'title']
            example.append(example3)
            if (count < length):
                train.append(example)
            else:
                ch_flag = random.randint(1, 10)
                if (ch_flag < 9):
                    test.append(example)
                else:
                    train.append(example)
            count+=1

    train_s=sorted(train, key=lambda line: line[0])
    test_s=sorted(test, key=lambda line: line[0])

    f = open('datasets/RecommendationSystem/movielens/train.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    for line in train_s:
        csv_writer.writerow(line)
    f.close()

    f = open('datasets/RecommendationSystem/movielens/test.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    for line in test_s:
        csv_writer.writerow(line)
    f.close()
    os.system('python fewshot.py --result_file ./output_fewshot.txt --dataset movielens --template_id 3 --seed 141 --shot 10 --verbalizer manual --max_epochs 7 --uid {} --rate_num {}'.format(uid,len(train_s)+len(test_s)))
    #]break