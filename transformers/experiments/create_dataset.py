import os
import json

path = "../../Datasets"

def main(filename, src, trg, dest_src, dest_trg):
    source = []
    target = []
    with open(filename, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.strip()
            dict = json.loads(d)
            if len(dict['translation'][src]) > 0 and len(dict['translation'][trg]) > 0:
                source.append(dict['translation'][src])
                target.append(dict['translation'][trg])

    if len(source) != len(target):
        print("incorrect length")
        return

    with open(dest_src, 'w') as f:
        for sent in source:
            f.write(sent+"\n")
    with open(dest_trg, 'w') as f:
        for sent in target:
            f.write(sent+"\n")

    print("successfullt finished")

def read(path):
    f = None
    with open(path, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.strip()
            f = json.loads(d)
    if f:
        k = list(f['translation'].keys())
        src = k[0]
        trg = k[1]
        return src, trg
    else:
        print("Error occured while processing", path)
        exit()


for dir, _, files in os.walk(path):
    for file in files:
        if 'JHU bible data' in dir or 'domain_relatedness' in dir or len(file)==0:
            continue
        path = os.path.join(dir, file)
        print(path)
        src, trg = read(path)
        dest_src = os.path.join(dir.replace('../../Datasets', './dataset'), file.split('.')[0]+'_'+src+'.txt')
        dest_trg = os.path.join(dir.replace('../../Datasets', './dataset'), file.split('.')[0]+'_'+trg+'.txt')
        main(path, src, trg, dest_src, dest_trg)
        if os.path.exists(path.replace('../../Datasets', './dataset')):
            os.remove(path.replace('../../Datasets', './dataset'))

os.rename('./dataset/Afrikaans', './dataset/af')
os.rename('./dataset/Assamese', './dataset/as')
os.rename('./dataset/French', './dataset/fr')
os.rename('./dataset/Hindi', './dataset/hi')
os.rename('./dataset/Irish', './dataset/ga')
os.rename('./dataset/Kannada', './dataset/te')
os.rename('./dataset/Sinhala', './dataset/si')
os.rename('./dataset/Tamil', './dataset/ta')
os.rename('./dataset/Xhosa', './dataset/xh')
os.rename('./dataset/Yoruba', './dataset/sw')
