from flask import Flask, request, render_template
import pickle
import re
import pandas as pd
from random import randint


app = Flask(__name__)


def data_preprocessing():

    #load the database
    anime_db = pd.read_csv('MAL_final.csv')
    anime_db.fillna('', inplace=True)
    
    #check missing values
    #anime_db.isnull().sum().sort_values(ascending=False)/len(anime_db)
    
    #replace missing ratings with average
    #anime_db['rating'].fillna(anime_db["rating"].median(),inplace = True)
    
    #replace missing types with 'T/M' which stands for TV or Movie
    #anime_db['type'].fillna('T/M',inplace = True)
    
    #remove special characters from the names
    #anime_db["name"] = anime_db["name"].map(lambda name:re.sub('[^A-Za-z0-9]+', " ", name))
    
    return anime_db

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/google7cbb854badf2aa11.html')
def googleVer():
	return render_template('google7cbb854badf2aa11.html')


@app.route('/randomAnime',methods=['GET', 'POST'])
def randomAnime():
	anime_db = data_preprocessing()
	if request.method == 'POST':
		R = randint(0,len(anime_db)-1)
		rand_anime = anime_db.iloc[R]
	else:
		R = randint(0,len(anime_db)-1)
		rand_anime = anime_db.iloc[R]

	#MAL = 'https://myanimelist.net/search/all?q={}'.format('+'.join(rand_anime['name'].split(' ')))
	return render_template('ratings.html',
			name = rand_anime['name'],
            english_name = rand_anime['english_name'],
			genre = rand_anime['genre'],
			ratings = round(rand_anime['rating'],2),
			type = rand_anime['type'],
			MAL_search=rand_anime['url'])
	

def animedict(anime_list):
	anime_dict = []
	for i in range(len(anime_list)):
		info = {
			"name": anime_list['name'][i],
            "english_name":anime_list['english_name'][i],
			"rating": round(anime_list['rating'][i],2),
			"genre": anime_list['genre'][i],
			"MAL": anime_list['url'][i]
		}
		anime_dict.append(info)
	return anime_dict


@app.route('/topAnimeMovies')
def topMovies():
	anime_db = data_preprocessing()
	TopM = anime_db[anime_db['type'] == 'Movie'][anime_db.members > 100].sort_values('rating',ascending=False).head(100)
	TopM = TopM.reset_index()
	TopM = TopM.drop(['index'],axis=1)
	topanime = animedict(TopM)

	return render_template("TopAnime.html",
						   title='Movies',
						   topanime=topanime)


@app.route('/topAnimeTV')
def topTV():
	anime_db = data_preprocessing()
	TopM = anime_db[anime_db['type'] == 'TV'][anime_db.members > 100].sort_values('rating',ascending=False).head(100)
	TopM = TopM.reset_index()
	TopM = TopM.drop(['index'],axis=1)
	topanime = animedict(TopM)

	return render_template("TopAnime.html",
						   title='TV Series',
						   topanime=topanime)

@app.route('/similarByName',methods=['POST'])
def similar_by_name():
	anime_db = data_preprocessing()
	if request.method == 'POST':
		result = request.form
	query = result['name']
	n = 0
	anime_list = []
	print('Anime with the words "{}" in the title:'.format(query))
	for i, name in enumerate(anime_db.name):
		if query.lower() in name.lower():
			info = {
				"name": anime_db['name'][i],
                "english_name": anime_db['english_name'][i],
				"rating": round(anime_db['rating'][i],2),
				"genre": anime_db['genre'][i],
				"type": anime_db['type'][i],
				"MAL": anime_db['url'][i]
			}
			anime_list.append(info)
			n+=1
	return render_template("similarAnime.html",
						   title='Name',
						   name=query,
						   topanime=anime_list)


@app.route('/similarByContent',methods=['POST'])
def similar_by_content():
	anime_db = data_preprocessing()
	if request.method == 'POST':
		result = request.form
	query = result['name']

	#load the model file
	pkl_file = open('anime_indices.pkl', 'rb')
	indices = pickle.load(pkl_file)
	if query not in anime_db['name']:
		N = anime_db[anime_db['name'] == query].index[0]
		anime_list = []
		for n in indices[N][1:]:
			info = {
				"name": anime_db['name'][n],
                "english_name": anime_db['english_name'][n],
				"rating": round(anime_db['rating'][n],2),
				"genre": anime_db['genre'][n],
				"type": anime_db['type'][n],
				"MAL": anime_db['url'][n]
			}
			anime_list.append(info)

		return render_template("similarAnime.html",
						   title='Content',
						   name=query,
						   topanime=anime_list)




if __name__ == '__main__':
	app.run()

