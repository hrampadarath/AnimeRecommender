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
from tqdm import tqdm
from time import sleep
from bs4.element import NavigableString, Tag



def extractNavigableStrings(context):
    """ from https://stackoverflow.com/questions/29110820/how-to-scrape-between-span-tags-using-beautifulsoup"""
    strings = []
    for e in context.children:
        if isinstance(e, NavigableString):
            strings.append(e)
        if isinstance(e, Tag):
            strings.extend(extractNavigableStrings(e))
    return strings



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
    
    df = pd.DataFrame(columns=["name","english_name","type","episodes","members","score_members", "rating","genre","dates", "url"])
    i = 0
    for result in results:
        #print(i)
        url_= result.find(class_="hoverinfo_trigger fl-l fs14 fw-b")["href"]
        html_ = requests.get(url_)
        soup_ = BeautifulSoup(html_.content, 'html.parser', from_encoding="utf-8")
        
        t1name = extractNavigableStrings(soup_.find(class_="h1-title"))
        if len(t1name) == 1:
            name = t1name[0]
            english_name = None
        elif len(t1name) >= 2:
            name=t1name[0]
            english_name=t1name[1]
        else:
            name = None
            english_name = None
            
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
        #try:
        #    score_members = float(soup_.find(class_="borderClass").find_all("span", itemprop="ratingCount")[0].text.strip())
        #except:
         #   score_members = None
        
        df = df.append({
            "name": name,
            "english_name":english_name,
            "type": Type_,
            "episodes": eps,
            "members": members,
            #"score_members": score_members,
            "rating": score,
            "genre": genres,
            "dates": Dates,
            "url": url_
        },ignore_index=True)
        
        i+=1
    return df


def webscrape_MAl(anime_limit=16750, start=0):
    url_template = "https://myanimelist.net/topanime.php?limit={}"
    df = pd.DataFrame(columns=["name","type","episodes","members","score_members", "rating","genre","dates"])
    for limit in tqdm(range(start,anime_limit, 50)): # iterate in steps of 50
        url = url_template.format(limit)
        df_temp = parse_MAl(url)
        if df_temp["name"].isnull().sum() >= 40:
            print("Number of missing names, for limit {} = {}".format(limit, df_temp["name"].isnull().sum()))
            print("--------Halting---------")
            raise SystemExit()
        save_mal_temp(df_temp, limit)
        
        # I think MAL has a limit on the number of conenctions per minute/second/hour
        # and after 200-400, the site blocks access. Adding the pause for 1 minute below soleves the issue
        sleep(60) # pause the loop for 1 minute. 
        





def save_mal_temp(df, limit):
    csvTemp = "temp/MAL_start_{}.csv".format(limit)
    df.to_csv(csvTemp)
        
    #print("Number of missing names, for limit {} = {}".format(limit, df["name"].isnull().sum()))
    
    

webscrape_MAl(anime_limit = 16750, start = 16550)