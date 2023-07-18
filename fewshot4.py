import pandas as pd
import numpy as np
import random
import csv
import os
random.seed(144)

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 3000)
movies=pd.read_csv('u.item',sep='|',names=['movie id','movie title','release date','video release date',
              'IMDb URL','unknown','Action','Adventure','Animation',
              'Children\'s','Comedy','Crime','Documentary','Drama','Fantasy',
              'Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi',
              'Thriller','War','Western'])
users=pd.read_csv('u.user',sep='|',names=['userId','age','gender','occupation','zip code'])
ratings=pd.read_csv('u.data',sep='\t',names=['userId','movie id','rating','timestamp'])

print(movies)
print(ratings)

label=['great','good','common','bad','awfully']
data = pd.merge(ratings,movies,on='movie id')
print(data)
data.insert(3,'mood',None)
a=set(data['userId'])
'''       
for index, row in data.iterrows():
    if(5>=float(row['rating'])>4):
        data.loc[index,'mood']='great'
    elif(4.5>=float(row['rating'])>3):
        data.loc[index,'mood']='good'
    elif(4>=float(row['rating'])>2):
        data.loc[index,'mood']='common'
    elif(3>=float(row['rating'])>1):
        data.loc[index,'mood']='bad'
    else:
        data.loc[index,'mood']='awfully'
'''

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
            # example3 = ' '.join(datal.loc[index, 'genres'].split("|")) + ' movie ' + datal.loc[index, 'title']
            genres=['Action','Adventure','Animation',
              'Children\'s','Comedy','Crime','Documentary','Drama','Fantasy',
              'Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi',
              'Thriller','War','Western']
            genres_all=[]
            for item in genres:
                if datal.loc[index, item]==1:
                    genres_all.append(item)
            example3 = ' '.join(genres_all)  + ' movie ' +datal.loc[index, 'movie title']
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
    os.system('python fewshot.py --result_file ./output_fewshot.txt --dataset movielens --template_id 3 --seed 141 --shot 10 --verbalizer manual --max_epochs 5 --uid {} --rate_num {}'.format(uid,len(train_s)+len(test_s)))
    #]break