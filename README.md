# Auto-tagger

Tag documents. Automatically.

## Data

[Facebook Recruiting - Keyword Extraction](https://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction/data)

## Processing steps

### Replace `'\n'` by `' '` (whitespace) and `'\r\n'` by `'\n'` to make the files more amenable to parsing by frameworks that expect one data point per line.

```
$ cat Train.csv | tr '\n' ' ' | tr '\r\n' '\n' > TrainClean.csv
```

### Break the file into 100 pieces to make debugging easier.

```
$ split -n 100 TrainClean.csv pieces/
```



