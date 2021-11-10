import kss
import pandas as pd
import os

data = []

def search(dirname):
    file_names = os.listdir(dirname)
    targets = []
    for file_name in file_names:
        full_filename = os.path.join(dirname, file_name)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.txt': 
            targets.append(full_filename)
    return targets

def split(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        sentences = f.readlines()

    data = []
    for s in sentences:
        for ss in kss.split_sentences(s):
            data.append(ss)

    pd.DataFrame(data).to_csv(file_name[:-4] + '.csv', encoding='utf-8')

targets = search('./')

for target in targets:
    split(target)