import pandas as pd
import geopy.distance 

df = pd.read_csv(r'places.txt', header=None, names = ['long','lat'])

df['coords'] = ''
df[0] = 0
df[1] = 0
df[2] = 0
df['cluster'] = 0

for i in range(len(df)):
    df['coords'][i] = (df['lat'][i],df['long'][i])

# Randomly initialize three centers
c0 = df['coords'][15]
c1 = df['coords'][107]
c2 = df['coords'][245]

count = 0

while count < 50:
    # Calculate the distances between each point and the three initial centers 
    for i in range(len(df)):
        df[0][i] = geopy.distance.vincenty(c0, df['coords'][i]).km
        df[1][i] = geopy.distance.vincenty(c1, df['coords'][i]).km
        df[2][i] = geopy.distance.vincenty(c2, df['coords'][i]).km
    
    # The cluster each point belongs to
    df['cluster'] = df[[0,1,2]].idxmin(axis=1)
    
    # Define the function to find out the new center point of each cluster
    def new_center(cluster):
        new_df = df[df['cluster']==cluster]
        new_df = new_df.reset_index(drop=True)
        new_center = (new_df['lat'].sum()/len(new_df),new_df['long'].sum()/len(new_df))
        
        for i in range(len(new_df)):
            new_df['cluster'][i] = geopy.distance.vincenty(new_center, new_df['coords'][i]).km
         
        new_center = new_df['cluster'].idxmin(axis=0)
        return new_df.iloc[new_center]['coords']
    
    # Assign the new center of each cluster to c0, c1, c2
    c0 = new_center(0)
    c1 = new_center(1)
    c2 = new_center(2)
    
    # Loop from the beginning using the new centers' lat long
    count += 1
    
result = df['cluster']
result.to_csv('clusters.txt',sep='\t')

# Visualize the result
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(8,8))
sns.scatterplot(x="lat", y="long", hue='cluster', data=df)
plt.ylabel('longitude')
plt.xlabel('latitude')
plt.legend(loc='lower right')
plt.show()