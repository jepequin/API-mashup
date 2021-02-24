import requests
import sys
import csv

def get_titles():
	'''Uses listener loop to let user input movie titles.
	   Returns dictionary whose key:value pairs are title:list of recommended movies'''
	recommended = {} 
	stop_input = False
	while not stop_input:
		movie = input('Type name of movie (press "Enter" if done): ')
		if movie == '':
			stop_input = True
		else:
			recommended[movie.lower()] = []
	return recommended

def get_apikey():
	'''Lets user input apikey. Returns such key'''
	apikey = input('Please input OMDB api key or press the "Enter" key: ')
	if apikey == '':
		print('Get a OMDB key at: https://www.omdbapi.com/')
		sys.exit()
	return apikey

def omdb_apikey_test(apikey,omdb_base_url):
	'''Tests if apikey input is valid. Exits program in the negative'''
	apikey_test_params = {'t':'pulp fiction','type':'movie', 'apikey':apikey}
	apikey_test_response = requests.get(omdb_base_url,params=apikey_test_params)
	apikey_test_dict = apikey_test_response.json()
	if 'Error' in apikey_test_dict:
		print(apikey_test_dict['Error'])
		print('Get a OMDB key at: https://www.omdbapi.com/')
		sys.exit()

def get_recommendation(recommended,tastedive_url,tastedive_params,omdb_url,omdb_params):
	'''Returns list of unknown movie titles and adds recommendations to known titles'''
	unknown_movies = []
	for movie in recommended:	
		tastedive_params['q'] = movie
		tastedive_response = requests.get(tastedive_base_url,params=tastedive_params)
		tastedive_dict = tastedive_response.json()
		if len(tastedive_dict['Similar']['Results']) < 1:
			'''List tastedive_dict['Similar']['Results'] is empty if movie title is unknown'''
			movie_title = tastedive_dict['Similar']['Info'][0]['Name']
			unknown_movies.append(movie_title.lower())
			print('Movie title "{}" is unknown (check for typos)'.format(movie_title))
		else:
			'''List tastedive_dict['Similar']['Results'] contains recommendations if movie title is known'''
			for media in tastedive_dict['Similar']['Results']:
				movie_title = media['Name']
				omdb_params['t'] = movie_title
				## Getting rotten tomatoes score for recommended movies
				omdb_response = requests.get(omdb_base_url,params=omdb_params)
				omdb_dict = omdb_response.json()
				rotten_score = omdb_dict['Ratings'][1]['Value']
				recommended[movie].append((movie_title,rotten_score))
			## Sorting recommended movies according to rotten tomatoes score	
			recommended[movie].sort(key = lambda tup:tup[1], reverse = True)
	return unknown_movies, recommended

def delete_misspelt_titles(unknown_movies,recommended):
	'''Deletes movies contained in "unknown_movies" list from "recommended" dictionary'''
	for movie_title in unknown_movies:
		del recommended[movie_title]
	return recommended

def csv_format(dictionary):
	'''Creates list of csv strings using keys of dictionary as row headers'''
	csv_rows = ['\n']
	for key in dictionary:
		row = key
		for tup in dictionary[key]:
			row = row + ',{}({})'.format(tup[0],tup[1])
		row = row + '\n'
		csv_rows.append(row)
	return csv_rows

def dump_csv(recommended):
	'''Dumps recommended movie titles to csv file'''
	with open('recommended_movies.csv','w') as csv_file:
		csv_rows = csv_format(recommended)
		for row in csv_rows:
			csv_file.write(row)

## Set base urls 
tastedive_base_url = 'https://tastedive.com/api/similar'
omdb_base_url = 'http://www.omdbapi.com/'

## Obtain movie titles, ombd apikey and verify key is valid
recommended = get_titles()
apikey = get_apikey()
omdb_apikey_test(apikey,omdb_base_url)

## Set parameters for query  
tastedive_params = {'type': 'movies', 'limit': '5'}
omdb_params = {'type':'movie', 'apikey':apikey}	

## Get recommended movies, get rid of misspelt titles and dump recommendations to csv
unknown_movies, recommended = get_recommendation(recommended,tastedive_base_url,tastedive_params,omdb_base_url,omdb_params)
recommended = delete_misspelt_titles(unknown_movies,recommended)
dump_csv(recommended)

