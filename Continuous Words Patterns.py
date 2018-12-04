# I only wrote the code for 1-gram pattern and 2-gram pattern. We can use the same logic to mine more patterns where n>2.

import pandas as pd

review = pd.read_csv("reviews_sample.txt",header=None,names=['sentence'])

### Frequent 1-gram pattern

# Store distinct words in each row in a set
review['word_set'] = review['sentence'].apply(lambda x: set(x.split(' '))) 

# Create bags of 1-gram words
words = []  
for i in range(len(review)):
    for j in review.loc[i]['word_set']:
        words.append(j) 

# Count distinct 1-gram words
from collections import Counter
counts = Counter(words)

counts_df = pd.DataFrame(list(counts.items()), columns = ['Words', 'Counts'])
counts_df.sort_values(by=['Counts'],ascending=0,inplace=True)

# Frequent 1-gram words with support > 99
itemset1 = counts_df[counts_df['Counts']>99]

### Frequent 2-gram pattern

# Break each row in 2 continuous words, get the set
review['words'] = review['sentence'].apply(lambda x: x.split(' '))

review['two_words'] = ''

for i in range(len(review)):
    count = 0
    words = []
    while count < len(review.loc[i]['words'])-1:
        words.append(review.loc[i]['words'][count] + ' ' + review.loc[i]['words'][count+1])
        count+=1
    review.loc[i]['two_words'] = words

review['two_words_set'] = review['two_words'].apply(lambda x: set(x)) 

# Create bags of 2-gram words
words2 = []  
for i in range(len(review)):
    for j in review.loc[i]['two_words_set']:
        words2.append( j ) 

# Count distinct 2-gram words 
from collections import Counter
counts = Counter(words2)

counts_df = pd.DataFrame(list(counts.items()), columns = ['Words', 'Counts'])
counts_df.sort_values(by=['Counts'],ascending=0,inplace=True)

# Frequent 2-gram words with support > 99
itemset2 = counts_df[counts_df['Counts']>99]

# Combine the frequent 1-gram patterns and 2-gram patterns
result = pd.concat([itemset1,itemset2])

# Create a column for the desired output format
result['Words'] = result['Words'].str.replace(" ", ";")
result['submit'] = result['Counts'].map(str) + ":" + result['Words'].map(str)

# Save the result in a txt file
result['submit'].to_csv('patterns.txt',header=None,index=False)