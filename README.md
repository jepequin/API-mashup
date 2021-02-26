# MOVIE RECOMMENDER

In this project we through the process of mashing up data from two different APIs to obtain a movie recommender. This is the final assignment for the course "Data Collection and Processing with Python". Its goal is to practice with the concepts introduced during the course: reading and understanding APIs documentation (finding base URLs, query parameters), requesting data from these APIs (using the requests module), extracting information from nested data structures (following the matra "understand, extract, repeat"), and others. Get more information at  https://www.coursera.org/learn/data-collection-processing-python/home/welcome.

## DESCRIPTION

An API mashup is an application that orchestrates multiple resources and methods from different APIs to create a new service displayed as a single API.

In this project we go through the process of mashing up data from two different APIs to make movie recommendations. The TasteDive API allows us to feed a movie (or bands, TV shows, etc.) as a query input, and returns a set of related items. The OMDB API accepts movie titles as a query input and get back data about the movie, including scores from various review sites (Rotten Tomatoes, IMDB, etc.).

Our program starts by asking the user to input (one by one) the names of the movies she wants to get recommendations for, as well as a OMBD apikey. It then proceeds to use TasteDive to get related movies for each title, and queries the OMDB API to get the Rotten Tomatoes scores of this list of related movies. Finally it sorts the recommendations according to their score and dumps the data to a csv (using as row header the movies the user wants recommendations for). 

It is worth mentioning that our code handles extreme cases. For instance:

- If the user inputs an invalid OMDB apikey, it ends execution and prints a message. 

- If a movie title with typos is fed, the code prevents the user the title was not recognized, and does not include it in the final csv.

The documentation for the API is at https://tastedive.com/read/api.

The documentation for the API is at https://www.omdbapi.com/

## AUTHOR

Jesua Epequin. Contact me at jesua.epequin@gmail.com  



