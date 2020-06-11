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

Update: 11/06/2020

Updated dataset webscraped from MAL and used to generate a new model. 
The model is saved as a.pkl file and loaded in this version, speeding up the processing

"""

import pandas as pd
import re
import pickle
from random import randint




def data():

    #load the database
    anime_db = pd.read_csv('data/MAL_final.csv')
    
    return anime_db




def Model():
    #oad saved model
    pkl_file = open('data/anime_indices.pkl', 'rb')
    indices = pickle.load(pkl_file)
    return indices


def pickle_predictions(indices):
    with open('anime_indices.pkl', 'wb') as fid:
        pickle.dump(indices, fid,2)


def similar_anime_content(query, indices, anime_db):
    if query not in anime_db['name']:
        N = anime_db[anime_db['name'] == query].index[0]
        print('Similar Anime to "{}": \n'.format(query))
        for n in indices[N][1:]:
            print('Anime: {} \n Genre: {}; Average ratings: {}; Format: {}, Members: {}'.format(anime_db.name[n],
                                                                                  anime_db.genre[n],
                                                                                  round(anime_db.rating[n],2),
                                                                                  anime_db['type'][n],
                                                                                  anime_db['members'][n]))
        
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
    

    
    
    