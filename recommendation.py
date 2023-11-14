from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import auc
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import streamlit as st

def read_csv(path=r'./ml-latest-small/'):
    """
    read csv file
    :param path:file path
    :return:csv data as DataFrame
    """
    try:
        data = pd.read_csv("data(1).txt")
        data.to_csv('data.csv', index=None )
    except:
        print('Open file error')
    return data

movie_ratingCount = (data.groupby(by = ['Movie'])['Rating'].
                     count().
                     reset_index().
                     rename(columns = {'Rating': 'totalRatingCount'})
                     [['Movie', 'totalRatingCount']])
movie_ratingCount.head()
rating_with_totalRatingCount = data.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
popularity_threshold = rating_with_totalRatingCount["totalRatingCount"].mean()
rating_popular_movie= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
movie_features_df=rating_popular_movie.pivot_table(index='title',columns='userId',values='rating').fillna(0)
from scipy.sparse import csr_matrix

movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)

def ww(m):
    for i, value in enumerate(movie_features_df.index):
        if m==value:
            query_index = i
            print(query_index)
            distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)
        else:
            pass
    return distances,indices,query_index
   
def main():
    global z
    while z:
        st.title("Movie Recommendation")
        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Movie Recommendation using streamlit </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)    
        #print(widget_ids_this_run)
        m = st.text_input("Enter the name and year of the movie","Type here",key='ab#@007!')
        if st.button("Predict"):
            result,result1,result2=ww(m)
            for i in range(0, len(result.flatten())):
                if i == 0:
                    st.text('Recommendations for {0}:\n'.format(movie_features_df.index[result2]))
                else:
                    st.text('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[result1.flatten()[i]], result.flatten()[i]))
            st.text("do you want to continue")
        if st.button("No"):
            st.text("Thank you for using our software")
            z=False
            break
        else:
            z=True
        
if __name__=="__main__":
    main()