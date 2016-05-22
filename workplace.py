# # import code; code.interact(local=locals())
from __future__ import division
import csv

class RatingsMuncher:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_data(self):
        raw_data = []
        with open(self.file_name, 'rU') as file:
            data = csv.DictReader(file)
            for row in data:
                raw_data.append(row)
        self.raw_data = raw_data

    def compute_probabilities(self):
        ratings = {'1':0,'2':0,'3':0,'4':0,'5':0}
        for viewing in self.raw_data:
            for num in ratings:
                if viewing['rating'] == num:
                    ratings[num] += 1
        for num in ratings:
            ratings[num] = ratings[num]/len(self.raw_data)
        self.check_prob(ratings)

    def check_prob(self,thing):
        sum = 0
        for num in thing:
            sum = sum + thing[num]
        if sum != 1:
            raise ValueError('A very specific bad thing happened... the probabilties dont add to 1')

    def collect_ids_of_ratings(self):
        ratings_movie_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        ratings_user_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        for viewing in self.raw_data:
            rating = viewing['rating']
            userID = viewing['userID']
            movieID = viewing['movieID']

            ratings_movie_ids[rating].append(movieID)
            ratings_user_ids[rating].append(userID)
        self.ratings_movies = ratings_movie_ids
        self.ratings_users = ratings_user_ids




class UsersMuncher:

    def __init__(self, file_name, ratings_users):
        self.file_name = file_name
        self.ratings_users = ratings_users

    def get_data(self):
        raw_data = []
        with open(self.file_name, 'rU') as file:
            data = csv.DictReader(file)
            for row in data:
                raw_data.append(row)
        self.raw_data = raw_data

    def compute_probabilities(self):
        ratings_list = ['1','2','3','4','5']
        ratings = {'data1':[],'data2':[],'data3':[],'data4':[],'data5':[]}
        prob_data = {'male':0, 'female':0, 'age1':0,'age18':0,'age25':0,'age35':0,'age45':0,'age56':0}
        for i in ratings_list:
            for user in self.ratings_users[i]:
                user.gender





class DataMuncher:

    def __init__(self, ratings_muncher):
        self.ratings_muncher = ratings_muncher
        ratings_users = self.ratings_muncher.ratings_users
        user_minion = UsersMuncher("users.csv", ratings_users)
        user_minion.get_data()
        self.user_minion = user_minion

    def compute_probabilities(self):
        self.user_minion.compute_probabilities




minion = RatingsMuncher("ratings.csv")
minion.get_data()
minion.compute_probabilities()
minion.collect_ids_of_ratings()


top_minion = DataMuncher(minion)
top_minion.compute_probabilities()

# import code; code.interact(local=locals())

#find probabilities for the ratings (categories)
#   probability of a 1,2,3,4,5
#find probabilities for each set of features for each category
#   for instance, for ratings of 1, what are the probability
#   that the user was male vs female,
#   that the user was 25 vs 45 vs 18 vs 35 vs 50 vs 1 vs 56
#       so action step: collect all userIDs and all movieIDs for ratings of 1
#to predict, take the user info and the movie info and multiply
#the probabilities for each category and pick the largest