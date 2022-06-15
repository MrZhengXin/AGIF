import pandas as pd
import json

df = pd.read_excel('multi-intent-dataset.xlsx')
instance_list = []
for _, row in df.iterrows():
    if type(row['Q1']) != str or type(row['Q2']) != str or type(row['Q3']) != str:
        continue
    q_list = [row['Q1'].strip(), row['Q2'].strip(), row['Q3'].strip()]
    if type(row['Q4']) is str:
        q_list.append(row['Q4'].strip())
    instance = {
        'text': row['sentence'],
        'summary': ';'.join(q_list) + ';'
    }
    instance_list.append(json.dumps(instance, ensure_ascii=False))

from sklearn.model_selection import train_test_split

train, dev = train_test_split(instance_list, test_size=1500)
dev, test = train_test_split(dev, test_size=1000)
with open('train.json', 'w', encoding='utf-8') as f:
    print(*train, file=f, sep='\n')

with open('test.json', 'w', encoding='utf-8') as f:
    print(*test, file=f, sep='\n')

with open('dev.json', 'w', encoding='utf-8') as f:
    print(*dev, file=f, sep='\n')