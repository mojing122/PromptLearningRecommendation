import os

for i in [10, 15, 20, 25]:
    for j in [10, 15, 20, 25, 30, 35]:
        os.system(
            'python t1.py --result_file ./output_fewshot.txt --dataset minds --template_id 3 --seed 141 --shot {} --verbalizer manual --max_epochs {}'.format(
                i, j))
