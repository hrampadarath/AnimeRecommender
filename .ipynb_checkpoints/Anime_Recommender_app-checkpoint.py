#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 23:58:07 2017

@author: H.Rampadarath

A basic content Anime recommender system 

The dataset used in here contains information 
on user preference data from 73,516 users on 12,294 anime from MyAnimeList.net. 
Each user is able to add anime to their completed list and 
give it a rating and this data set is a compilation of those ratings. 

The data was sourced from MAL and made available through Kaggle.
The data set is dated around December 2016.

This contains 3 files:
    This file - the executor file
    Anime_Recommender.py - the main code
    anime.csv - the database

"""

import Anime_Recommender

def menu():
    user_input = input("Select 'N' to search for an anime by name \n"
                       "'M' to list the top Anime Movies by average ratings\n"
                       "'A' to list the top Anime TV series by average ratings\n"
                       "'S' to generate a list of Anime that is smiliar to another \n"
                       "'R' Do you feel lucky? \n"
                       "'Q' to quit \n")
    
    N = int(input("Enter the number of recommendations: \n"))
    print('Plese wait while we build the model')
    anime_db = Anime_Recommender.data_preprocessing()
    anime_features = Anime_Recommender.features(anime_db)
    indices = Anime_Recommender.Model(anime_features,N)
    while user_input != 'Q':

        if user_input == 'N':
            query = input('Enter your query:\n')
            Anime_Recommender.similar_anime_by_name(query,anime_db)
            
        elif user_input == 'M':
            Anime_Recommender.TopAnimeMovie(anime_db,N)
        
        elif user_input == 'A':
            Anime_Recommender.TopAnimeTV(anime_db,N)
            
        elif user_input == 'S':
            query = input('Enter the Anime:\n')
            Anime_Recommender.similar_anime_content(query,indices,anime_db)
        elif user_input == 'R':
            Anime_Recommender.randomAnime(anime_db)
        
        user_input = input("Select 'N' to search for an anime by name \n"
                       "'M' to list the top Anime Movies by average ratings\n"
                       "'A' to list the top Anime TV series by average ratings\n"
                       "'S' to generate a list of Anime that is smiliar to another \n"
                       "'R' Do you feel lucky? \n"
                       "'Q' to quit \n")
        


menu()