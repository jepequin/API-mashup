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
		recommended[movie] = []

apikey = input('Please input OMDB api key or press the "Enter" key: ')
if apikey == '':
	print('Get a OMDB key at: https://www.omdbapi.com/')
	sys.exit()

tastedive_base_url = 'https://tastedive.com/api/similar'
tastedive_params = {'type': 'movies', 'limit': '5'}
omdb_base_url = 'http://www.omdbapi.com/'
omdb_params = {'type':'movie', 'apikey':apikey}

for movie in recommended:	
	tastedive_params['q'] = movie
	tastedive_response = requests.get(tastedive_base_url,params=tastedive_params)
	tastedive_dict = tastedive_response.json()
	for media in tastedive_dict['Similar']['Results']:
		movie_title = media['Name']
		omdb_params['t'] = movie_title
		omdb_response = requests.get(omdb_base_url,params=omdb_params)
		omdb_dict = omdb_response.json()
		rotten_score = omdb_dict['Ratings'][1]['Value']
		recommended[movie].append((movie_title,rotten_score))
	recommended[movie].sort(key = lambda tup:tup[1], reverse = True)

def csv_format(dictionary):
	csv_rows = []
	for key in dictionary:
		row = key
		for tup in dictionary[key]:
			row = row + ',{}({})'.format(tup[0],tup[1])
		row = row + '\n'
		csv_rows.append(row)
	return csv_rows

with open('recommended_movies.csv','w') as csv_file:
    csv_rows = csv_format(recommended)
    csv_file.write('\n')
    for row in csv_rows:
    	csv_file.write(row)

#6f2bc66d
