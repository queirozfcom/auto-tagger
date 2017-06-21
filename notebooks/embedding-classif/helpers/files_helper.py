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

def read_glove_wiki(d=100):
    
    supported_dimensions = [50,100,200,300]
    
    if d not in supported_dimensions:
        raise ValueError("argument d must be one of {0}".format(",".join(supported_dimensions)))
    
    
    GLOVE_DIR = "/media/felipe/SAMSUNG/GloVe"
    embeddings_index = {}

    with open(os.path.join(GLOVE_DIR,"glove.6B.{0}d.txt".format(d)),'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:],dtype='float32')

            embeddings_index[word] = coefs
            
    return embeddings_index

def read_glove_wiki_weighted(d,weight_index):
    supported_dimensions = [50,100,200,300]
    
    if d not in supported_dimensions:
        raise ValueError("argument d must be one of {0}".format(",".join(supported_dimensions)))
    
    
    GLOVE_DIR = "/media/felipe/SAMSUNG/GloVe"
    embeddings_index = {}

    matches = 0
    overall = 0
    
    with open(os.path.join(GLOVE_DIR,"glove.6B.{0}d.txt".format(d)),'r') as f:
        for line in f:
            values = line.split()
            word = values[0]       
            coefs = np.asarray(values[1:],dtype='float32')

            maybe_weight = weight_index.get(word)
            
            if maybe_weight is None:
                weight = 1.0
            else:
                weight = maybe_weight
                matches += 1
                        
            overall +=1        
            embeddings_index[word] = coefs * weight
           
    print("overall, {0} out of {1} embeddings were weighted. Total available embeddings: {2}".format(matches, len(weight_index), overall))
    
    return embeddings_index    

def read_glove_stackoverflow(): 
    
    GLOVE_DIR = "/media/felipe/SAMSUNG/StackGlove"
    embeddings_index = {}

    with open(os.path.join(GLOVE_DIR,"glove.stackoverflow.7B.50d.txt"),'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:],dtype='float32')

            embeddings_index[word] = coefs
            
    return embeddings_index

def read_glove_stackoverflow_weighted(weight_index):
    
    GLOVE_DIR = "/media/felipe/SAMSUNG/StackGlove"
    embeddings_index = {}

    matches = 0
    overall = 0
    
    with open(os.path.join(GLOVE_DIR,"glove.stackoverflow.7B.50d.txt"),'r') as f:
        for line in f:
            values = line.split()
            word = values[0]       
            coefs = np.asarray(values[1:],dtype='float32')

            maybe_weight = weight_index.get(word)
            
            if maybe_weight is None:
                weight = 1.0
            else:
                weight = maybe_weight
                matches += 1
                        
            overall +=1        
            embeddings_index[word] = coefs * weight
           
    print("overall, {0} out of {1} embeddings were weighted. Total available embeddings: {2}".format(matches, len(weight_index), overall))
    
    return embeddings_index    


def read_stackoverflow_sample_small_stanford_tokenized():
    """
    Returns tokenized texts (title+body) and their respective tags.
    
    usage: 
        texts, tags = files_helper.read_stackoverflow_sample_small_stanford_tokenized()  
    
    """
        
    path_to_file = "/media/felipe/SAMSUNG/StackHeavy/Posts-shuffled/Small-Sample-Posts-Shuffled-Stanford-Tokenized.csv"
    
    texts = []
    labels = []

    with open(path_to_file,'r') as f:
        reader = csv.reader(f,quotechar='"', delimiter=',',
                     escapechar='\\', skipinitialspace=True)

        for line in reader:
            id,text,tags = line[0],line[1],line[2].strip(',')

            texts.append(text)
            tags_array = [t.strip() for t in tags.split(',')]
            labels.append(tags_array)

    return (texts,labels)


def read_stackoverflow_sample_small(join=True):
    """
    Returns documents and their respective tags.
    
    If join is True, then titles and bodies are concatenated (with a 
    space separator) into a single string.
    
    usage: 
        texts, tags = files_helper.read_stackoverflow_sample_small()
        titles,bodies,tags = files_helper.read_stackoverflow_sample_small(join=False)
    
    
    """
        
    path_to_file = "/media/felipe/SAMSUNG/StackHeavy/Posts-shuffled/Small-Sample-Posts-Shuffled.csv"
    
    
    titles = []
    bodies = []
    texts = []
    labels = []

    with open(path_to_file,'r') as f:
        reader = csv.reader(f,quotechar='"', delimiter=',',
                     escapechar='\\', skipinitialspace=True)

        for line in reader:
            id,title,body,tags = line[0],line[1],line[2],line[3].strip(',')

            if join is True:
                text = title + " " + body
                texts.append(text)
            else:
                titles.append(title)
                bodies.append(body)
                
            tags_array = [t.strip() for t in tags.split(',')]
            labels.append(tags_array)

    if join is True:
        return (texts,labels)
    else:
        return (titles,bodies,labels)

def read_stackoverflow_sample_medium():
    path_to_file = "/media/felipe/SAMSUNG/StackHeavy/Posts-shuffled/Medium-Sample-Posts-Shuffled.csv"

    texts = []
    labels_index = {}
    labels = []

    with open(path_to_file,'r') as f:
        reader = csv.reader(f,quotechar='"', delimiter=',',
                     escapechar='\\', skipinitialspace=True)

        for line in reader:
            id,title,body,tags = line[0],line[1],line[2],line[3].strip(',')

            text = title + " " + body

            tags_array = [t.strip() for t in tags.split(',')] 

            texts.append(text)
            labels.append(tags_array)

    return(texts,labels)   

            
     