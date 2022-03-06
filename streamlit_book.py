import streamlit as st
import pandas as pd
import pickle
import time

import turicreate as tc
from streamlit import caching


st.set_page_config(page_title="Book Recommender System", page_icon="🐞", layout="centered")
st.header("🐞 Book Recommender System!")
st.subheader('This app will recommend you books based on what you read and liked')

@st.cache 
def loaddata():
    df = pd.read_csv('dfrecom.csv')
    df["ProductId"] = df["ProductId"].astype(str)
    #Creating dataframe to make dictionary of books IDs and book titles 
    dfdict = df.iloc[:,[4,5,6]].copy()
    dfdict = dfdict.drop_duplicates()
    dfdict.index = range(len(dfdict))
    #These lists are for the dropbown menus
    listofbooks = list(dfdict["Book-Title"].unique())
    listofauthors = list(dfdict["Book-Author"].unique())
    return df, dfdict, listofbooks, listofauthors

model = tc.load_model("RS.model")

df, dfdict, listofbooks, listofauthors = loaddata()
IDtoNameDict = dict(zip(list(dfdict.ProductId),list(dfdict["Book-Title"])))

#first book choosing
col_one_list_tit = listofbooks
col_one_list_auth = listofauthors
selectbox_title = st.selectbox('Please choose the book title', col_one_list_tit, index=0,key="1")
selectbox_author = st.selectbox('Please choose the author', col_one_list_auth, index=0,key="1")

cols_1 = st.columns((1, 1))

book1 = list(dfdict[(dfdict["Book-Author"]==selectbox_author)&(dfdict["Book-Title"] ==selectbox_title)].iloc[:,2])


if cols_1[0].button("Submit",key="1"):
    if len(book1) != 0:
        item1 = list(dfdict[(dfdict["Book-Author"]==selectbox_author)&(dfdict["Book-Title"] ==selectbox_title)].iloc[:,2])[0]
    else:
        st.write("There are no books satisfying your search!")

 #second book choosing       
col_two_list_tit = listofbooks
col_two_list_auth = listofauthors
selectbox_title2 = st.selectbox('Please choose the book title', col_two_list_tit, key="2")
selectbox_author2 = st.selectbox('Please choose the author', col_two_list_auth, index=0, key="2")

cols_2 = st.columns((1, 1))

book2 = list(dfdict[(dfdict["Book-Author"]==selectbox_author2)&(dfdict["Book-Title"] ==selectbox_title2)].iloc[:,2])        
        
        
if cols_2[0].button("Submit",key="2"):
    if len(book2) != 0:
        item2 = list(dfdict[(dfdict["Book-Author"]==selectbox_author2)&(dfdict["Book-Title"] ==selectbox_title2)].iloc[:,2])[0]
    else:
        st.write("There are no books satisfying your search!")  
  
#third book choosing       
col_three_list_tit = listofbooks
col_three_list_auth = listofauthors
selectbox_title3 = st.selectbox('Please choose the book title', col_three_list_tit, key="3")
selectbox_author3 = st.selectbox('Please choose the author', col_three_list_auth, index=0, key="3")

cols_3 = st.columns((1, 1))

book3 = list(dfdict[(dfdict["Book-Author"]==selectbox_author3)&(dfdict["Book-Title"] ==selectbox_title3)].iloc[:,2])        
        
        
if cols_3[0].button("Submit",key="3"):
    if len(book3) != 0:
        item3 = list(dfdict[(dfdict["Book-Author"]==selectbox_author3)&(dfdict["Book-Title"] ==selectbox_title3)].iloc[:,2])[0]
    else:
        st.write("There are no books satisfying your search!")
    

    
    
listofproducts = [item1, item2, item3]
#Making recommendation for books according to cosine similarity, passing the listofproducts to reommend
recommendation_item = model.get_similar_items(items=listofproducts, k=10)
#Creating dataframe
dfitem = pd.DataFrame(recommendation_item)
#Data manipulation and transformation to show the top 10 books to recommend
dfitem['item_occ'] = dfitem.groupby('similar').similar.transform('count')
dfitem = dfitem.sort_values(["item_occ", "score"],ascending=(False,False))
dfitem = dfitem[~dfitem["similar"].isin(listofproducts)]
dfitem = dfitem.drop_duplicates(subset=['similar', "item_occ"])
dfitem.index = range(len(dfitem))
dfitem = dfitem.drop(columns=["ProductId", "score", "rank", "item_occ"])
dfitem = dfitem.replace({"similar":IDtoNameDict})
dfitem = dfitem.rename(columns={"similar":"recommended books"})
st.write("These are the books you might be interested in, based on your previously liked books:")
st.table(dfitem.head())

 



        
