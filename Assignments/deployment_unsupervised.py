## import packages for this
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import tqdm
from tqdm.notebook import tqdm_notebook
import os.path
from sklearn.preprocessing import MinMaxScaler
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import kaleido
import plotly.express as px
import plotly.io as pio
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

df=pd.read_csv("/Users/rebeccaharrison/Documents/Python/Bootcamp/Data/country_data/Country-data.csv")
df.rename(columns={'child_mort': 'Under 5 mortality','inflation':'Inflation', 'income': 'Net income per person','life_expec':'Life expectancy','total_fer':'Fertility rate','gdpp':'GDP per capita'}, inplace=True)
## headings for our data application
st.title('Is your selected country eligible for aid?')
st.sidebar.header('You have selected')


# Scaling the data (#)
scaler_X = MinMaxScaler() # this is often a really good one to use, but the industry standard is the standard scaler
df_scaled = scaler_X.fit_transform(df.iloc[:,1:10]) # Scaling  data

# creating the k means model with 3 clusters on full data
kmeans2=KMeans(n_clusters=2,init='k-means++',random_state=0)
cluster2=kmeans2.fit_predict(df_scaled)
df.loc[:,'cluster2']=cluster2

df['clusterfinal']=""
df['clusterfinal'].loc[df['cluster2'] == 1 ]= 'Richest'
df['clusterfinal'].loc[df['cluster2'] == 0 ]='Poorest'

# Creating the hierarchical clustering
hierarchical2 = AgglomerativeClustering(n_clusters = 2, affinity = 'euclidean', linkage = 'ward')
hiercluster2 = hierarchical2.fit_predict(df_scaled)

df['hiercluster2']=hiercluster2
df['hierclusterfinal']=""
df['clustercombined']=""


df['hierclusterfinal'].loc[df['hiercluster2'] == 0 ]= 'Richest'
df['hierclusterfinal'].loc[df['hiercluster2'] == 1 ]= 'Poorest'


df['cluster2combined']=""

df.loc[(df['hierclusterfinal'] == 'Richest') & (df['clusterfinal'] == 'Richest'),'cluster2combined']= 'Richest'
df.loc[(df['hierclusterfinal'] == 'Richest') & (df['clusterfinal'] != 'Richest'),'cluster2combined']= 'Poor/rich'
df.loc[(df['hierclusterfinal'] != 'Richest') & (df['clusterfinal'] == 'Richest'),'cluster2combined']= 'Poor/rich'
df.loc[(df['hierclusterfinal'] == 'Poorest') & (df['clusterfinal'] == 'Poorest'),'cluster2combined']= 'Poorest'



countries=df.iloc[:,0]
#Function that accepts users input
def user_report():
    country = st.select_slider(
     'Which country you are interested in?',
     options=countries)    
    return country


# Country Data
user_country = user_report()
kmeans_cluster = df.loc[:,'clusterfinal'][df.loc[:,'country'] == user_country ].values[0]
hierarchical_cluster = df.loc[:,'hierclusterfinal'][df.loc[:,'country'] == user_country ].values[0]

st.sidebar.write(user_country)
# write cluster
st.sidebar.header('Which K means cluster does this fall under?')
st.sidebar.write(kmeans_cluster)
st.sidebar.header('Which hierarchical cluster does this fall under?')
st.sidebar.write(hierarchical_cluster)

fig, ax = plt.subplots(1, 6, sharey=False, figsize=[20, 4])
variables = list(df.iloc[:,[1,5,6,7,8,9]].columns)

sns.set_style("whitegrid")
df['selected']=""
df['selected'].loc[df['country'] == user_country ]='Country selected'
cluster=df.loc[:,'cluster2'][df.loc[:,'country'] == user_country ].values[0]

st.subheader('How does this country score on key metrics compared to other countries?')
i=0
fig.suptitle('Data variation by country grouped with k means clustering')
for var in variables:
    country_value=df.loc[:,var][df.loc[:,'country'] == user_country ].values[0]
    sns.violinplot(x="clusterfinal", y=var, data=df, ax=ax[i])
 #   sns.stripplot(x="clusterfinal", y=var, hue="selected", data=df, s = 3,jitter=0.05,ax=ax[i])
    ax[i].set_title(var)
    ax[i].set_xlabel("Cluster")
    ax[i].set_ylabel("")
    ax[i].annotate(user_country,
            xy=(cluster, country_value), xycoords='data',
            xytext=(.5, .5), textcoords='axes fraction',
            horizontalalignment="center",
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            color="red"),
            bbox=dict(boxstyle="round", fc="w"),
            )

    ax[i].legend([],[], frameon=False)
    i+=1
st.pyplot(fig)



## Output
output = ''
if kmeans_cluster=="Poorest" and hierarchical_cluster=="Poorest": 
    output = 'This country is eligible for aid'
elif kmeans_cluster=="Richest" and hierarchical_cluster=="Richest":
    output = 'This country is not eligible for aid'
else:
    output = 'This country may be eligible for aid under certain circumstances'
st.subheader(output)

# Creating the map to display

fig2 = px.choropleth(df[['country','cluster2combined']],
                    locationmode='country names',
                    locations='country',
                    title='Which countries are in which clusters?',
                    hover_name="country",
                    color_discrete_sequence=["orange", "red", "green",'black'],color=df['cluster2combined'], 

                    color_discrete_map={'Poorest':'Red',
                                        'Richest':'Green',
                                        'Poor/rich':'Orange'} )
fig2.update_geos(fitbounds="locations", visible=True)

fig2.update_layout(legend_title_text='Labels',legend_title_side='top',title_pad_l=260,title_y=0.86)

#fig2.show(engine='kaleido')
st.plotly_chart(fig2)
