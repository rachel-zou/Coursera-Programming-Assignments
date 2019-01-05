import pandas as pd
from sklearn.metrics.cluster import normalized_mutual_info_score

partitions = pd.read_csv(r'partitions.txt',header=None,names = ['id','cluster'], sep='\s+')
c1 = pd.read_csv(r'clustering_1.txt',header=None,names = ['id','cluster'], sep='\s+')
c2 = pd.read_csv(r'clustering_2.txt',header=None,names = ['id','cluster'], sep='\s+')
c3 = pd.read_csv(r'clustering_3.txt',header=None,names = ['id','cluster'], sep='\s+')
c4 = pd.read_csv(r'clustering_4.txt',header=None,names = ['id','cluster'], sep='\s+')
c5 = pd.read_csv(r'clustering_5.txt',header=None,names = ['id','cluster'], sep='\s+')

clusters = [c1,c2,c3,c4,c5]
nmi = []
jss = []

for c in clusters:
    FP=0; FN=0; TP=0; #TN=0;
    for i in range(len(partitions)):
        for j in range(len(c)):
            if j > i and partitions['cluster'][i] == partitions['cluster'][j] and c['cluster'][i] == c['cluster'][j]:
                TP += 1
            elif j > i and partitions['cluster'][i] != partitions['cluster'][j] and c['cluster'][i] == c['cluster'][j]:
                FP += 1
            elif j > i and partitions['cluster'][i] == partitions['cluster'][j] and c['cluster'][i] != c['cluster'][j]:
                FN += 1
            #elif j > i and partitions['cluster'][i] != partitions['cluster'][j] and c['cluster'][i] != c['cluster'][j]:
                #TN += 1
    nmi.append(round(normalized_mutual_info_score(partitions['cluster'], c['cluster']),7))
    #print(TN)
    jss.append(round(TP/(TP+FN+FP),7))
    
score = pd.DataFrame({'nmi':nmi,'jss':jss})
score.to_csv('scores.txt', sep=' ', index=False, header=False, encoding='utf-8')
