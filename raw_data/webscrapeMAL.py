#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:07:07 2020

@author: Hayden Rampadarath (haydenrampadarath@gmail.com)

Script to webscrape My Anime List
"""


import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

def parse_MAl(url):
    """
    Parameters
    ----------
    url : string
        myanimelist.net url string 

    Returns
    -------
    df : DataFrame
        returns a dataframe with columns "name","type","episodes","members","score_members", "rating","genre","dates"

    """
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    results = soup.find_all(class_= "ranking-list")
    
    df = pd.DataFrame(columns=["name","type","episodes","members","score_members", "rating","genre","dates"])
    i = 0
    for result in results:
        #print(i)
        url_= result.find(class_="hoverinfo_trigger fl-l fs14 fw-b")["href"]
        html_ = requests.get(url_)
        soup_ = BeautifulSoup(html_.content, 'html.parser', from_encoding="utf-8")
        
        try:
            name = soup_.find(class_="h1-title").text.strip()
        except:
            name = None
            
        Type, Dates, members = result.find(class_="information di-ib mt4").text.strip().splitlines()
        try:
            members = float("".join(members.split()[0].split(",")))
        except:
            members = None
            
        [Type_, eps, n] = [", ".join(x.split()) for x in re.split(r'[()]',Type)]
        
        try:
            eps = float(eps.split(",")[0])
        except:
            eps = None
        
        try:
            genres = [genre.text.strip() for genre in soup_.find(class_="borderClass").find_all("span", itemprop="genre")]
            
        except:
            genres = None
        
        try:
            score = float(soup_.find(class_="borderClass").find_all("span", itemprop="ratingValue")[0].text.strip())
        except:
            score = None
        try:
            score_members = float(soup_.find(class_="borderClass").find_all("span", itemprop="ratingCount")[0].text.strip())
        except:
            score_members = None
        
        df = df.append({
            "name": name,
            "type": Type_,
            "episodes": eps,
            "members": members,
            "score_members": score_members,
            "rating": score,
            "genre": genres,
            "dates": Dates
        },ignore_index=True)
        
        i+=1
    return df


def webscrape_MAl(limit=16750):
    url_template = "https://myanimelist.net/topanime.php?limit={}"
    df = pd.DataFrame(columns=["name","type","episodes","members","score_members", "rating","genre","dates"])
    for start in range(0,limit, 50): # iterate in steps of 50
        url = url_template.format(start)
        df_temp = parse_MAl(url)
        df = df.append(df_temp, ignore_index=True)
    # save to disk
    
    df.to_csv('My_Anime_List_uncleaned.csv', encoding='utf-8')



webscrape_MAl()
