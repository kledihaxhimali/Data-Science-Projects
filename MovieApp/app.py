import pandas as pd
import joblib
import streamlit as st 
import warnings
from warnings import filterwarnings
filterwarnings("ignore")

def load_data():
    data=pd.read_csv('movie_data.csv')
    dataframe=pd.read_csv('movie_dataframe.csv')
    return data, dataframe

    
def load_models():
    sig=joblib.load('sigmoid_kernel.pkl')
    tfv=joblib.load('tfidf_vectorizer.pkl')
    return sig, tfv


data,dataframe=load_data()
sig, tfv= load_models()
print(data['original_title'])


def give_recommendations(movie_title, model, data, dataframe):
  indicies= pd.Series(data = data.index, index=data['original_title'])
  idx=indicies[movie_title]
  model_score= list(enumerate(model[idx]))
  model_scores_sorted= sorted(model_score, key=lambda x: x[1], reverse=True)
  model_scores_10= model_scores_sorted[1:11]
  movie_indices_10= [i[0] for i in model_scores_10]
  return dataframe['original_title'][movie_indices_10]


st.set_page_config(page_title= "Simple Movie Recommender", layout = "centered")
st.title("🎥 Movie Recommendations")
st.write('Movie suugestion based on what you have watched!')
movie_list= data['original_title'].sort_values().tolist()
selected_movie=st.selectbox('Select a movie: ', movie_list)

if st.button('Get Recommandations'):
    if selected_movie:
        recommendations=give_recommendations(selected_movie, sig, data, dataframe)
        st.subheader("MPvies similar to: "+ selected_movie)
        for index, movie in enumerate(recommendations):
            
            st.write(str(index + 1) + '. '+ movie)

st.markdown("________")
st.markdown("This app uses Content based filtering!")
