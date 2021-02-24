import requests
import sys
import csv
from pprint import pprint

recommended = {} 
stop_input = False
while not stop_input:
	movie = input('Type name of movie (press "Enter" if done): ')
	if movie == '':
		stop_input = True
	else:
		recommended[movie.lower()] = []

apikey = input('Please input OMDB api key or press the "Enter" key: ')
if apikey == '':
	print('Get a OMDB key at: https://www.omdbapi.com/')
	sys.exit()
tastedive_base_url = 'https://tastedive.com/api/similar'
tastedive_params = {'type': 'movies', 'limit': '5'}
omdb_base_url = 'http://www.omdbapi.com/'
omdb_params = {'type':'movie', 'apikey':apikey}	

omdb_test_params = omdb_params.copy()
omdb_test_params['t'] = 'pulp fiction'
omdb_test_response = requests.get(omdb_base_url,params=omdb_test_params)
omdb_test_dict = omdb_test_response.json()
if 'Error' in omdb_test_dict:
	#pprint(omdb_test_dict)
	#print(omdb_test_response.url)
	print(omdb_test_dict['Error'])
	print('Get a OMDB key at: https://www.omdbapi.com/')
	sys.exit()

unknown_movies = []
for movie in recommended:	
	tastedive_params['q'] = movie
	tastedive_response = requests.get(tastedive_base_url,params=tastedive_params)
	tastedive_dict = tastedive_response.json()
	if len(tastedive_dict['Similar']['Results']) < 1:
		movie_title = tastedive_dict['Similar']['Info'][0]['Name']
		unknown_movies.append(movie_title)
		print('Movie title "{}" is unknown (check for typos)'.format(movie_title))
	else:
		for media in tastedive_dict['Similar']['Results']:
			movie_title = media['Name']
			omdb_params['t'] = movie_title
			omdb_response = requests.get(omdb_base_url,params=omdb_params)
			omdb_dict = omdb_response.json()
			rotten_score = omdb_dict['Ratings'][1]['Value']
			recommended[movie].append((movie_title,rotten_score))
		recommended[movie].sort(key = lambda tup:tup[1], reverse = True)

for movie_title in unknown_movies:
	del recommended[movie_title.lower()]

def csv_format(dictionary):
	csv_rows = ['\n']
	for key in dictionary:
		row = key
		for tup in dictionary[key]:
			row = row + ',{}({})'.format(tup[0],tup[1])
		row = row + '\n'
		csv_rows.append(row)
	return csv_rows

with open('recommended_movies.csv','w') as csv_file:
    csv_rows = csv_format(recommended)
    for row in csv_rows:
    	csv_file.write(row)

#6f2bc66d
