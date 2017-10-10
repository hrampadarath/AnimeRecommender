#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 23:29:44 2017

@author: H.Rampadarath

A basic content Anime recommender system 

The dataset used in here contains information 
on user preference data from 73,516 users on 12,294 anime from MyAnimeList.net. 
Each user is able to add anime to their completed list and 
give it a rating and this data set is a compilation of those ratings. 

The data was sourced from MAL and made available through Kaggle.
The data set is dated around December 2016.
"""

import pandas as pd
import re
import pickle
from random import randint




def data_preprocessing():

    #load the database
    anime_db = pd.read_csv('anime.csv')
    
    #check missing values
    anime_db.isnull().sum().sort_values(ascending=False)/len(anime_db)
    
    #replace missing ratings with average
    anime_db['rating'].fillna(anime_db["rating"].median(),inplace = True)
    
    #replace missing types with 'T/M' which stands for TV or Movie
    anime_db['type'].fillna('T/M',inplace = True)
    
    #remove special characters from the names
    anime_db["name"] = anime_db["name"].map(lambda name:re.sub('[^A-Za-z0-9]+', " ", name))
    
    return anime_db


def features(anime_db):

    #The features we will be using for the system are the genre, type and the ratings
    anime_features = pd.concat([anime_db.genre.str.get_dummies(sep=","),
                                pd.get_dummies(anime_db['type']),anime_db.rating],axis=1)
    
    #use MaxBsScaler to scale the features from 1-0, while preserving sparsity
    from sklearn.preprocessing import MaxAbsScaler
    max_abs_scaler = MaxAbsScaler()
    anime_features = max_abs_scaler.fit_transform(anime_features)
    
    return anime_features


def Model(anime_features, K):

    #build the ML model using the unsupervised verion of K-Nearest Neighbors
    from sklearn.neighbors import NearestNeighbors

    nn_model = NearestNeighbors(n_neighbors=K,algorithm='auto').fit(anime_features)
    
    #Obtain the indices of and distances to the the nearest K neighbors of each point.
    distances, indices = nn_model.kneighbors(anime_features)
    pickle_predictions(indices)
    
    return indices


def pickle_predictions(indices):
    with open('anime_indices.pkl', 'wb') as fid:
        pickle.dump(indices, fid,2)


def similar_anime_content(query, indices, anime_db):
    if query not in anime_db['name']:
        N = anime_db[anime_db['name'] == query].index[0]
        print('Similar Anime to "{}": \n'.format(query))
        for n in indices[N][1:]:
            print('Anime: {} \n Genre: {}; Average ratings: {}; Format: {} \n'.format(anime_db.name[n],
                                                                      anime_db.genre[n],
                                                                      anime_db.rating[n],anime_db['type'][n])) 
        
    else:
        print('The anime {} does not exist in our database.'.format(query))



def similar_anime_by_name(query, anime_db):  
    n = 0
    print('Anime with the words "{}" in the title:'.format(query))
    for i, name in enumerate(anime_db.name):
        if query in name:
            print('Anime: {}; Format: {}'.format(anime_db.name[i],anime_db['type'][i]))
            n+=1
    if n == 0:
        print('No anime with a name similar to "{}" exists in our database.'.format(query))


def TopAnimeTV(anime_db, N):
    TopA = anime_db[anime_db['type'] == 'TV'][anime_db.members > 100].sort_values('rating',ascending=False).head(N)
    TopA = TopA.drop(['anime_id','type','episodes'],axis=1)
    print(TopA)

def TopAnimeMovie(anime_db, N):
    TopM = anime_db[anime_db['type'] == 'Movie'][anime_db.members > 100].sort_values('rating',ascending=False).head(N)
    TopM = TopM.drop(['anime_id','type','episodes'],axis=1)
    print(TopM)
    
    
def randomAnime(anime_db):
    R = randint(0,len(anime_db)-1)
    rand_anime = anime_db.iloc[R]
    print('Random Anime: {}; Genre: {}'.format(rand_anime['name'],rand_anime['genre']))
    print('Average ratings: {}; Format: {}'.format(rand_anime['rating'],rand_anime['type']))
    

    
    
    