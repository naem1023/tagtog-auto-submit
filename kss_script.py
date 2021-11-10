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

    print(sentences)
    # for s in sentences:
    #     kss.split_sentences(s)

        

targets = search('.\\')

print(kss.split_sentences("색소폰(Saxophone, Sax)은 클라리넷과 같이 하나의 리드가 들어있는 취구를 사용하는 목관악기이다."))
split('색소폰.txt')
print(targets)

