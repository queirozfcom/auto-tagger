import os 
import sys
import numpy as np
import csv

def read_20_newgroup_files():
    
    path_to_data_directory = "/home/felipe/data/20_newsgroup/20_newsgroup/"
    
    texts = []
    labels_index = {}
    labels = []
    
    for name in sorted(os.listdir(path_to_data_directory)):
        path = os.path.join(path_to_data_directory,name)
        
        if os.path.isdir(path):
            label_id = len(labels_index)
            labels_index[name] = label_id
            
            for fname in sorted(os.listdir(path)):
                if fname.isdigit():
                    fpath = os.path.join(path, fname)
                    if sys.version_info < (3,):
                        f = open(fpath)
                    else:
                        f = open(fpath, encoding='latin-1')
                    t = f.read()
                    i = t.find('\n\n')
                                       
                    if i > 0:
                        t = t[i:]
                                     
                
                    texts.append(t)
                    f.close()
                    labels.append(label_id)                    
        
        
    return (texts,labels_index,labels)

def read_glove_100():
    GLOVE_DIR = "/media/felipe/SAMSUNG/GloVe"
    embeddings_index = {}

    with open(os.path.join(GLOVE_DIR,"glove.6B.100d.txt"),'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:],dtype='float32')

            embeddings_index[word] = coefs
            
    return embeddings_index

def read_stackoverflow_sample_small():
    path_to_file = "/media/felipe/SAMSUNG/StackHeavy/Small-Sample-Posts-csv/Small-Sample-Posts.csv"

    texts = []
    labels_index = {}
    labels = []

    with open(path_to_file,'r') as f:
        reader = csv.reader(f,quotechar='"', delimiter=',',
                     escapechar='\\', skipinitialspace=True)

        for line in reader:
            id,title,body,tags = line[0],line[1],line[2],line[3].strip(',')

            text = title + " " + body

            tags_array = tags.split(',') 

            texts.append(text)
            labels.append(tags_array)

    return(texts,labels)             
            
     