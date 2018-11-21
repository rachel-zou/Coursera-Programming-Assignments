# Import libraries
import pandas as pd
from mlxtend.frequent_patterns import apriori

# Load dataset
df = pd.read_csv('categories.txt',sep='\t',header=None,names=['categories'])
df.reset_index(inplace=True)

# Split each record into single record and store each record in a row
df_index_list = []
df_categories_list = []

for i in range(len(df)):
    for j in range(len(df.loc[i,'categories'].split(';'))):
        df_index = {}
        df_categories = {}
        df_index['index'] = i
        df_categories['categories'] = df.loc[i,'categories'].split(';')[j]
        df_index_list.append(df_index)
        df_categories_list.append(df_categories)
        
df = pd.DataFrame(df_index_list).join(pd.DataFrame(df_categories_list))

# Prepare data in the format apriori needs
df['occurance'] = 1
itemsets = df.groupby(['index','categories'])['occurance'].sum().unstack().reset_index().fillna(0).set_index('index')

# The dataset is ready. Now we find the frequent item sets with minimum support 0.01
frequent_itemsets = apriori(itemsets, min_support=0.01, use_colnames=True)

# Prepare the data format we can upload
frequent_itemsets['count'] = round(frequent_itemsets['support']*77185,0) 
frequent_itemsets['result'] = ""

for i in range(len(frequent_itemsets)):
    frequent_itemsets.loc[i, 'result'] = ";".join(frequent_itemsets.loc[i,'itemsets'])
    frequent_itemsets.loc[i, 'result'] = frequent_itemsets.loc[i,'count'].astype(int).astype(str) + ":" + frequent_itemsets.loc[i,'result']
       
frequent_itemsets['result'].to_csv('Frequent Itemset Mining using Apriori.txt',index=False)

#### Single Frequent Items
# Find the single frequent items with minimum support 0.01
count = df['categories'].value_counts().reset_index()
count = count[count['categories']>771]
count['count'] = ''

for i in range(len(count)):
    count.loc[i, 'count'] = count.loc[i,'categories'].astype(int).astype(str) + ":" + count.loc[i,'index']
       
count['count'].to_csv('Frequent Single Item Mining.txt',index=False)