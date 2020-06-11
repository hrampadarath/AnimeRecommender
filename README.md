# AnimeRecommender

A basic content based Anime recommender system, using the Nearest Neighbors algorithm, and data webscraped from MyAnimeList.net. 

### Version 1

The first version of this app was developed about 3 years ago as a sort of way to get personall recommendations for my next anime. The first version used data from MAL that was uploaded to Kaggle, and dated around December 2016 (https://www.kaggle.com/CooperUnion/anime-recommendations-database). The dataset is located at data/anime.csv
That dataset contains information on user preference data from 73,516 users on 12,294 anime. The app can be run in two ways:

1. run the file Anime_Recommender_app.py. 
2. use the Flask webapp, deployed to Heroku at: https://anime-recommender-app.herokuapp.com/

The original development of the recommender system is located at notebooks/Anime_Recommender_orig.ipynb



### Version 2: in progress

The new version of this app is currently being developed:

- webscraper:files are in the raw_data folder under webscrapeMAP.py (webscraper) and webscrape_MyAnime.ipynb (for info on how the webscraper was developed).
- Model development: notebooks/Anime_Recommender.ipynb
- data: MAL.csv (raw data from the webscraper); MAL_name_miss.csv (entries with the anime name missing from MAL.csv, and was manually added); MAL_name_miss.csv (MAL.csv updated with the missing names); MAL_update_rating.csv (update of MAL_update.csv with missing ratings added using a linear model)


