import requests
import sys
from pprint import pprint


tastedive_base_url = 'https://tastedive.com/api/similar'
params = {'q': 'pulp fiction', 'type': 'movies', 'limit': '10'}
tastedive_response = requests.get(tastedive_base_url,params=params)
tastedive_dict = tastedive_response.json()
#pprint(tastedive_dict['Similar']['Info'])
#pprint(tastedive_dict['Similar']['Results'])

similar_movies = []
for media in tastedive_dict['Similar']['Results']:
	similar_movies.append(media['Name'])

#print(similar_movies)

apikey = input('Please input OMDB api key or press the "Enter" key: ')
if apikey== '':
	print('Get a OMDB key at: https://www.omdbapi.com')
	sys.exit()

omdb_base_url = 'http://www.omdbapi.com/'
params = {'type':'movie', 'apikey':apikey}
rotten_scores = []
for movie_title in similar_movies:
	params['t'] = movie_title
	omdb_response = requests.get(omdb_base_url,params=params)
	omdb_dict = omdb_response.json()
	#print(omdb_dict.keys())
	#print(omdb_dict['Ratings'])
	rotten_score = omdb_dict['Ratings'][1]['Value']
	rotten_scores.append(rotten_score)

print(rotten_scores)
similar_movies_scores = zip(similar_movies,rotten_scores)
sorted_movies = sorted(similar_movies_scores,key = lambda tup:tup[1])
print(sorted_movies)
